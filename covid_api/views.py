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
    track_query = await models.db.select([
        models.Track.id,
        models.Track.user_id,
        models.Track.health_status,
        models.Track.created,
        ga.func.ST_X(ga.func.ST_Dump(models.Track.geo_points).geom),
        ga.func.ST_Y(ga.func.ST_Dump(models.Track.geo_points).geom),
        ga.func.ST_Z(ga.func.ST_Dump(models.Track.geo_points).geom),
    ]).gino.all()
    track_results = {}
    for tid, uid, health, created, lat, lng, ts in track_query:
        if tid not in track_results:
            track_results[tid] = {
                'id': tid,
                'points': [],
                'user_id': uid,
                'health_status': health,
                'created': created
            }
        track_results[tid]['points'].append({
            'coord': {
                'lat': lat,
                'lng': lng
            },
            'timestamp': int(ts)
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
    logger.debug(track)
    points = []
    for point in track.points:
        ts = utils.datetime_to_timestamp(point.timestamp)
        points.append(f'{point.coord.lat} {point.coord.lng} {ts}')
    geo_points = 'MultiPointZ({})'.format(','.join(points))
    uid = track.user_id
    logger.debug(f'Adding track for user {uid}: {geo_points}')
    await models.Track.create(
        user_id=uid,
        geo_points=geo_points,
        health_status=track.health_status,
    )
    return response.json({'success': True})
