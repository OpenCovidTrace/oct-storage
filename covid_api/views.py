import decimal
import geoalchemy2 as ga

from sanic import response
from sanic.exceptions import ServerError
from sanic.log import logger

from .app import app
from . import models, utils


@app.route('/')
async def yo(request):
    return response.text('yo')


@app.route('/tracks/')
async def get_tracks(request):
    track_query = await models.db.select([
        models.Track.id,
        models.Track.user_id,
        models.Track.created,
        ga.func.ST_X(ga.func.ST_Dump(models.Track.linestring).geom),
        ga.func.ST_Y(ga.func.ST_Dump(models.Track.linestring).geom),
        ga.func.ST_Z(ga.func.ST_Dump(models.Track.linestring).geom),
    ]).gino.all()
    logger.debug(track_query[0])
    track_results = {}
    for tid, uid, created, lat, lng, ts in track_query:
        if tid not in track_results:
            track_results[tid] = {
                'id': tid,
                'points': [],
                'user_id': uid,
                'created': created
            }
        track_results[tid]['points'].append({
            'coord': {
                'lat': lat,
                'lng': lng
            },
            'timestamp': ts
        })
    return response.json({
        'tracks': list(track_results.values())
    }, dumps=utils.json_dumps)


@app.route('/tracks/', methods=['POST'])
async def upload_track(request):
    data = request.json
    points = []
    try:
        assert 'user_id' in data
        assert 'points' in data
    except AssertionError:
        raise ServerError('Missing `user_id` or `points` in request data', status_code=400)
    for point in data['points']:
        try:
            ts = int(point['timestamp'])
        except (KeyError, ValueError, AttributeError):
            raise ServerError(f'Invalid point {point}', status_code=400)
        with utils.precision_context(7):
            try:
                lng = decimal.Decimal(repr(point['coord']['lng']))
                lat = decimal.Decimal(repr(point['coord']['lat']))
            except (KeyError, ValueError, AttributeError):
                raise ServerError(f'Invalid point coord {point}', status_code=400)
            points.append(f'{lat} {lng} {ts}')
    if points:
        linestring = 'MultiPointZ({})'.format(','.join(points))
        print(linestring)
        uid = data['user_id']
        logger.debug(f'Adding track for user {uid}: {linestring}')
        await models.Track.create(
            user_id=uid,
            linestring=linestring
        )
    else:
        logger.info(f'Empty points in request {data}')
    return response.json({'success': True})
