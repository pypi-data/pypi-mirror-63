import sanic
import logging
logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


def _get_from_query(request, name_of_param, required=False):
    param = request.args.get(name_of_param)
    if not param and required:
        raise ValueError(f'Missing {name_of_param} query parameter')

    return param


def _get_from_header(request, name_of_header, required=False):
    header_value = request.headers.get(name_of_header)
    if not header_value and required:
        raise ValueError(f'Missing {name_of_header} header')

    return header_value


def _pre_validation(params):
    prefix = 'sanic-function-deps'
    if type(params) != list:
        raise ValueError(f'{prefix}: helper params must be list')

    for idx, param in enumerate(params):
        if type(param) == dict:
            txt = '{}: Missing \'{}\' in helper params, index: {}'
            required_params = ['name', 'source']

            for _param in required_params:
                if _param not in param:
                    raise ValueError(txt.format(prefix, _param, idx))


def _process_args(request, params):
    values = []
    try:
        for param in params:
            if type(param) == str:
                values.append(
                    _get_from_query(
                         request,
                         name_of_param=param,
                         required=True
                    )
                 )
            elif type(param) == dict:
                source = param['source']
                if source == 'query':
                    values.append(
                        _get_from_query(
                            request,
                            name_of_param=param['name'],
                            required=param.get('required', True)
                        )
                    )
                elif source == 'header':
                    values.append(
                        _get_from_header(
                            request,
                            name_of_header=param['name'],
                            required=param.get('required', True)
                        )
                    )
    except ValueError as e:
        return {'msg': str(e)}

    return values


def function_deps(params):
    logger.debug(f'function deps {params}')
    _pre_validation(params)

    def wrap(consumer_function):
        # func is the app/route function of the actual user, not sanic.
        logger.debug(f'Outer consumer {consumer_function}')

        async def wrapped(request):
            # Now sanic has called our function. We will begin
            # processing here and vet our params
            logger.debug(f'Outer request {request}')
            args = _process_args(request, params)
            logger.debug(f'Outer processed: {args}, {type(args)}')
            if type(args) == dict:
                # It's an error
                logger.debug(f'Error! {args}')
                return sanic.response.json(args)
            else:
                logger.debug(f'Proccessed args {args}')
                return await consumer_function(*args)

        return wrapped

    return wrap
