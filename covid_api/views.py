import geoalchemy2 as ga

from sanic import response
from sanic.log import logger

import pydantic

from .app import app
from . import models, utils, forms
from . import web_exceptions as web_exc


@app.route('/')
async def yo(request):
    return response.text('yo')


@app.route('/tracks/')
async def get_tracks(request):
    try:
        filters = forms.TrackFilter(**dict(request.query_args))
    except pydantic.ValidationError as err:
        raise web_exc.InvalidData(data=err.errors())
    track_query = models.db.select([
        models.Track.id,
        models.Track.user_id,
        models.Track.health_status,
        models.Track.created,
        ga.func.ST_X(ga.func.ST_Dump(models.Track.geo_points).geom),
        ga.func.ST_Y(ga.func.ST_Dump(models.Track.geo_points).geom),
        ga.func.ST_Z(ga.func.ST_Dump(models.Track.geo_points).geom),
    ])
    if filters.lastUpdateTimestamp:
        track_query = track_query.where(
            models.Track.created > filters.lastUpdateTimestamp
        )
    if filters.timestamp:
        ts_from = utils.datetime_to_timestamp_ms(filters.timestamp)
    else:
        ts_from = None
    track_results = {}
    for tid, uid, health, created, lat, lng, ts in await track_query.gino.all():
        ts = int(ts)
        if ts_from is not None and ts < ts_from:
            continue
        if tid not in track_results:
            track_results[tid] = {
                'points': [],
                'userId': uid,
            }
        track_results[tid]['points'].append({
            'lat': lat,
            'lng': lng,
            'tst': ts,
        })
    return response.json({
        'tracks': list(track_results.values())
    }, dumps=utils.json_dumps)


@app.route('/tracks/', methods=['POST'])
async def upload_track(request):
    try:
        track = forms.Track(**request.json)
    except pydantic.ValidationError as err:
        raise web_exc.InvalidData(data=err.errors())
    points = []
    for point in track.points:
        logger.debug(point)
        ts = utils.datetime_to_timestamp_ms(point.tst)
        points.append(f'{point.lat} {point.lng} {ts}')
    geo_points = 'MultiPointZ({})'.format(','.join(points))
    uid = track.userId
    logger.debug(f'Adding track for user {uid}: {geo_points}')
    await models.Track.create(
        user_id=uid,
        geo_points=geo_points,
        health_status=track.healthStatus,
    )
    return response.json({'success': True})


@app.route('/contacts/')
async def get_contacts(request):
    try:
        filters = forms.ContactFilter(**dict(request.query_args))
    except pydantic.ValidationError as err:
        raise web_exc.InvalidData(data=err.errors())
    uid = filters.userId
    contacts = []
    contact_query = models.db.select([
        models.Contact.contact_user_id,
        models.Contact.contact_ts,
        ga.func.ST_X(models.Contact.geo_point),
        ga.func.ST_Y(models.Contact.geo_point),
    ]).where(models.Contact.user_id == uid)

    for contact_uid, ts, lat, lng in await contact_query.gino.all():
        contacts.append({
            'userId': contact_uid,
            'lat': lat,
            'lng': lng,
            'tst': utils.datetime_to_timestamp_ms(ts),
        })
    return response.json({'userId': uid, 'contacts': contacts})


@app.route('/contacts/', methods=['POST'])
async def upload_contact(request):
    try:
        user_contacts = forms.ContactBlock(**request.json)
    except pydantic.ValidationError as err:
        raise web_exc.InvalidData(data=err.errors())
    uid = user_contacts.userId
    for contact in user_contacts.contacts:
        await models.Contact.create(
            user_id=uid,
            contact_user_id=contact.userId,
            geo_point=f'Point({contact.lat} {contact.lng})',
            contact_ts=contact.tst
        )
    return response.json({'success': True})
