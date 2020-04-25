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
    ]).where(
        models.Track.geo_boundary.intersects(
            ga.func.ST_MakeEnvelope(
                filters.minLat, filters.minLng, filters.maxLat, filters.maxLng
            )
        )
    )
    if filters.lastUpdateTimestamp:
        track_query = track_query.where(
            models.Track.uploaded > filters.lastUpdateTimestamp
        )
    track_results = {}
    for tid, ukey, day, lat, lng, ts in await track_query.gino.all():
        ts = int(ts)
        if tid not in track_results:
            track_results[tid] = {
                'points': [],
                'day': utils.date_to_day_number(day),
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
        data = forms.TracksBlock(**request.json)
    except pydantic.ValidationError as err:
        raise web_exc.InvalidData(data=err.errors())
    for track in data.tracks:
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
        await models.db.status(models.db.text(
            'INSERT INTO tracks (anon_user_key, date_created, uploaded, geo_points, geo_boundary)'
            'VALUES (:key, :day, :uploaded, '
            ':geo_points, ST_MakeEnvelope(:min_lat, :min_lng, :max_lat, :max_lng))'
        ), dict(
            key=track.key,
            min_lat=min_lat,
            max_lat=max_lat,
            min_lng=min_lng,
            max_lng=max_lng,
            geo_points='MultiPointZ({})'.format(','.join(points)),
            day=track.day,
            uploaded=utils.utcnow()
        ))
    return response.json({'success': True})


@app.route('/keys/')
async def get_keys(request):
    try:
        filters = forms.KeyFilter(**dict(request.query_args))
    except pydantic.ValidationError as err:
        raise web_exc.InvalidData(data=err.errors())
    keys = []
    key_query = models.db.select([
        models.Key.user_key,
        models.Key.date_created,
        ga.func.ST_Xmin(models.Key.geo_boundary),
        ga.func.ST_Ymin(models.Key.geo_boundary),
        ga.func.ST_Xmax(models.Key.geo_boundary),
        ga.func.ST_Ymax(models.Key.geo_boundary),
    ]).where(
        models.Key.geo_boundary.intersects(
            ga.func.ST_MakeEnvelope(
                filters.minLat, filters.minLng, filters.maxLat, filters.maxLng
            )
        )
    )
    load_from = filters.lastUpdateTimestamp
    if load_from:
        key_query = key_query.where(
            models.Key.uploaded > load_from
        )
    for ukey, day, min_lat, min_lng, max_lat, max_lng in await key_query.gino.all():
        keys.append({
            'value': ukey,
            'day': utils.date_to_day_number(day),
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
        data = forms.KeysBlock(**request.json)
    except pydantic.ValidationError as err:
        raise web_exc.InvalidData(data=err.errors())
    for key in data.keys:
        await models.db.status(models.db.text(
            'INSERT INTO keys (user_key, date_created, uploaded, geo_boundary) VALUES '
            '(:key, :day, :uploaded, ST_MakeEnvelope(:min_lat, :min_lng, :max_lat, :max_lng))'
        ), dict(
            key=key.value,
            min_lat=key.border.minLat,
            max_lat=key.border.maxLat,
            min_lng=key.border.minLng,
            max_lng=key.border.maxLng,
            day=key.day,
            uploaded=utils.utcnow()
        ))
    return response.json({'success': True})
