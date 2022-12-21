from typing import Optional, Iterable, Dict, List, Tuple, Any, Union, SupportsIndex

from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError

from schemas import RequestParamListSchema
from utils import build_query


main_bp = Blueprint('main', __name__)


@main_bp.route('/perform_query', methods=['POST'])
def perform_query() -> Union[Response, Tuple[Any, str]]:

    try:
        params: Dict[str, List[Dict[str, str]]] = RequestParamListSchema().load(data=request.json)
    except ValidationError as error:
        return Response(response=error.messages, status=400)

    result: Optional[Iterable[str]] = None
    for query in params['queries']:
        result = build_query(
            cmd=query['cmd'],
            param=query['value'],
            filename=params['filename'],
            data=result,
        )

    return jsonify(result), '200'
