import geoalchemy2 as ga

from sanic import response

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
        models.Track.anon_user_key,
        models.Track.date_created,
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
    for tid, ukey, day, lat, lng, ts in await track_query.gino.all():
        ts = int(ts)
        if ts_from is not None and ts < ts_from:
            continue
        if tid not in track_results:
            track_results[tid] = {
                'points': [],
                'day': utils.datetime_to_timestamp(day),
                'key': ukey,
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
        tracks = forms.Tracks(**request.json)
    except pydantic.ValidationError as err:
        raise web_exc.InvalidData(data=err.errors())
    for track in tracks:
        points = []
        min_lat = max_lat = min_lng = max_lng = None
        for point in track.points:
            lng = point.lng
            lat = point.lat
            if min_lng is None or lng < min_lng:
                min_lng = lng
            if max_lng is None or lng > min_lng:
                max_lng = lng
            if min_lat is None or lat < min_lat:
                min_lat = lat
            if max_lat is None or lat > min_lat:
                max_lat = lat
            ts = utils.datetime_to_timestamp_ms(point.tst)
            points.append(f'{lat} {lng} {ts}')
        geo_points = 'MultiPointZ({})'.format(','.join(points))
        ukey = track.key
        await models.Track.create(
            anon_user_key=ukey,
            geo_points=geo_points,
            date_created=track.day,
            geo_boundary=f'ST_MakeEnvelop('f'{min_lat},{min_lng},{max_lat},{max_lng})'
        )
    return response.json({'success': True})


@app.route('/keys/')
async def get_keys(request):
    try:
        filters = forms.KeyFilter(**dict(request.query_args))
    except pydantic.ValidationError as err:
        raise web_exc.InvalidData(data=err.errors())
    keys = []
    key_query = models.db.select([
        models.Contact.user_key,
        models.Contact.date_created,
        ga.func.ST_X(models.Contact.geo_min),
        ga.func.ST_Y(models.Contact.geo_min),
        ga.func.ST_X(models.Contact.geo_max),
        ga.func.ST_Y(models.Contact.geo_max),
    ])
    load_from = filters.lastUpdateTimestamp
    if load_from:
        key_query = key_query.where(
            models.Contact.created > load_from
        )

    for ukey, day, min_lat, min_lng, max_lat, max_lng in await key_query.gino.all():
        keys.append({
            'value': ukey,
            'day': utils.datetime_to_timestamp(day),
            'border': {
                'minLat': min_lat,
                'minLng': min_lng,
                'maxLat': max_lat,
                'maxLng': max_lng,
            },
        })
    return response.json({'keys': keys})


@app.route('/keys/', methods=['POST'])
async def upload_key(request):
    try:
        keys = forms.Keys(**request.json)
    except pydantic.ValidationError as err:
        raise web_exc.InvalidData(data=err.errors())
    for key in keys:
        min_lat = key.border.min_lat
        max_lat = key.border.max_lat
        min_lng = key.border.min_lng
        max_lng = key.border.max_lng
        await models.Key.create(
            user_key=key.key,
            geo_boundary=f'ST_MakeEnvelop('f'{min_lat},{min_lng},{max_lat},{max_lng})'
        )
    return response.json({'success': True})
