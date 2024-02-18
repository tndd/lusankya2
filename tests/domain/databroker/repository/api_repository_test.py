from domain.databroker.model.api import ApiRequest, ApiResponse


def test_store_request(psql_client, databroker_api_repository):
    # api_requestを作成
    request_id = 'b90287e9-5478-f434-8eff-20613ae0d1c1'
    api_request = ApiRequest(
        endpoint='endpoint_a',
        parameter={'param_a': 'value_a'},
        header={'header_a': 'value_a'},
        id_=request_id,
        timestamp='2022-01-01 00:00:00'
    )
    # api_requestを保存
    databroker_api_repository.store_request(api_request)
    # api_requestが保存されたかの確認
    query_confirm_api_request = f"""
        SELECT id FROM databroker.api_request WHERE id = '{request_id}';
    """
    result = psql_client.execute(query_confirm_api_request)
    assert len(result) == 1


def test_store_response(psql_client, databroker_api_repository):
    """
    注意:
        api_responseの登録にはapi_requestを事前に登録する必要がある。
    """
    # api_requestを作成
    request_id = 'b90287e9-5478-f434-8eff-20613ae0d1c1'
    api_request = ApiRequest(
        endpoint='endpoint_a',
        parameter={'param_a': 'value_a'},
        header={'header_a': 'value_a'},
        id_=request_id,
        timestamp='2022-01-01 00:00:00'
    )
    # api_requestを保存
    databroker_api_repository.store_request(api_request)
    # api_responseを作成
    response_id = '4ae3bc1a-db11-14a3-8f35-75d112b8bd79'
    api_response = ApiResponse(
        request_id=request_id,
        status=200,
        header={'header_a': 'value_a'},
        body={'body_a': 'value_a'},
        id_=response_id,
        timestamp='2022-01-01 00:00:00'
    )
    # api_responseを保存
    databroker_api_repository.store_response(api_response)
    # api_requestが保存されたかの確認
    query_confirm_api_response = f"""
        SELECT id FROM databroker.api_response WHERE id = '{response_id}';
    """
    result = psql_client.execute(query_confirm_api_response)
    assert len(result) == 1


def test_store_request_and_response(psql_client, databroker_api_repository):
    # api_requestを作成
    request_id = '5473dd4e-be44-48a2-2f3b-58c99fd546c4'
    api_request = ApiRequest(
        endpoint='endpoint_a',
        parameter={'param_a': 'value_a'},
        header={'header_a': 'value_a'},
        id_=request_id,
        timestamp='2022-01-01 00:00:00'
    )
    # api_responseを作成
    response_id = '4178ccb9-bd28-a398-92a3-e38cfcb741d7'
    api_response = ApiResponse(
        request_id=request_id,
        status=200,
        header={'header_a': 'value_a'},
        body={'body_a': 'value_a'},
        id_=response_id,
        timestamp='2022-01-01 00:00:00'
    )
    # request,responseを同時に保存
    databroker_api_repository.store_request_and_response(api_request, api_response)
    # api_requestが保存されたかの確認
    query_confirm_api_request = f"""
        SELECT id FROM databroker.api_request WHERE id = '{request_id}';
    """
    result = psql_client.execute(query_confirm_api_request)
    assert len(result) == 1
    # api_requestが保存されたかの確認
    query_confirm_api_response = f"""
        SELECT id FROM databroker.api_response WHERE id = '{response_id}';
    """
    result = psql_client.execute(query_confirm_api_response)
    assert len(result) == 1


def test_fetch_todo_requests(psql_client, databroker_api_repository):
    """
    概要:
        未実行あるいは失敗したリクエストのみが取得されていることを確かめる

    登録するデータ:
        1. リクエストが成功している
        2. リクエストが失敗している
        3. リクエストが未実行
        4. １度目は失敗しているが、２度目は成功しているリクエスト
        5. ２度連続で失敗しているリクエスト

    期待されるレスポンス:
        - 2,3,5のみが取得される
        - 取得されるのはきちんと最新の情報であること
    """
    # リクエスト群の作成
    request1_success = ApiRequest(
        endpoint='red',
        parameter={'param_a': 'value_a'},
        header={'header_a': 'value_a'},
        id_='b90287e9-5478-f434-8eff-20613ae0d1c1',
        timestamp='2022-01-01 00:00:01'
    )
    request2_failed = ApiRequest(
        endpoint='red',
        parameter={'param_b': 'value_b'},
        header={'header_b': 'value_b'},
        id_='393cd9c8-e31c-8b45-561e-02c4fe4075ad',
        timestamp='2022-01-01 00:00:02'
    )
    request3_not_yet = ApiRequest(
        endpoint='blue',
        parameter={'param_c': 'value_c'},
        header={'header_c': 'value_c'},
        id_='5473dd4e-be44-48a2-2f3b-58c99fd546c4',
        timestamp='2022-01-01 00:00:03'
    )
    request4_failed_then_success = ApiRequest(
        endpoint='blue',
        parameter={'param_d': 'value_d'},
        header={'header_d': 'value_d'},
        id_='4178ccb9-bd28-a398-92a3-e38cfcb741d7',
        timestamp='2022-01-01 00:00:04'
    )
    request5_failed_twice = ApiRequest(
        endpoint='blue',
        parameter={'param_e': 'value_e'},
        header={'header_e': 'value_e'},
        id_='8f025e21-3a5f-f165-b747-cb1271ef95ce',
        timestamp='2022-01-01 00:00:05'
    )
    # リクエスト群の登録
    databroker_api_repository.store_request(request1_success)
    databroker_api_repository.store_request(request2_failed)
    databroker_api_repository.store_request(request3_not_yet)
    databroker_api_repository.store_request(request4_failed_then_success)
    databroker_api_repository.store_request(request5_failed_twice)
    # レスポンス群の作成
    response1_success = ApiResponse(
        request_id=request1_success.id_,
        status=200,
        header={'header_a': 'value_a'},
        body={'body_a': '一発成功'},
        id_='1603d215-b28f-29a8-d3f0-f4255c97ea8a',
        timestamp='2022-01-02 00:00:00'
    )
    response2_failed = ApiResponse(
        request_id=request2_failed.id_,
        status=400,
        header={'header_b': 'value_b'},
        body={'body_b': '一発失敗'},
        id_='9dcb8110-b8b9-f1f3-2414-d9b51a924baf',
        timestamp='2022-01-02 00:01:00'
    )
    response4_first_failed = ApiResponse(
        request_id=request4_failed_then_success.id_,
        status=400,
        header={'header_d': 'value_d'},
        body={'body_d': '１度目は失敗'},
        id_='5591cc75-0a36-6698-db3c-eadd06c11eeb',
        timestamp='2022-01-02 00:02:00'
    )
    response4_second_success = ApiResponse(
        request_id=request4_failed_then_success.id_,
        status=200,
        header={'header_d': 'value_d'},
        body={'body_d': '２度目は成功'},
        id_='4d62c4d1-f981-6e36-f28c-cc1cd560fc55',
        timestamp='2022-01-02 00:03:00'
    )
    response5_first_failed = ApiResponse(
        request_id=request5_failed_twice.id_,
        status=400,
        header={'header_e': 'value_e'},
        body={'body_e': '１度目失敗'},
        id_='77603482-cd64-12f1-7a28-8c1b1c50480d',
        timestamp='2022-01-02 00:04:00'
    )
    response5_second_failed = ApiResponse(
        request_id=request5_failed_twice.id_,
        status=400,
        header={'header_e': 'value_e'},
        body={'body_e': '２度目も失敗'},
        id_='fe613e5f-e4bb-fdd1-5753-9be1207a4173',
        timestamp='2022-01-02 00:05:00'
    )
    # レスポンス群の登録
    databroker_api_repository.store_response(response1_success)
    databroker_api_repository.store_response(response2_failed)
    databroker_api_repository.store_response(response4_first_failed)
    databroker_api_repository.store_response(response4_second_success)
    databroker_api_repository.store_response(response5_first_failed)
    databroker_api_repository.store_response(response5_second_failed)
    # リクエストの取得
    todo_requests = databroker_api_repository.fetch_todo_requests()
    # 取得されるのは、期待通りのIDであることを確認
    assert set([r.id_ for r in todo_requests]) == set([request2_failed.id_, request3_not_yet.id_, request5_failed_twice.id_])
    """
    エンドポイントの絞り込みのテスト:
        エンドポイントがblueのもののみが取得されることを確認。
        つまり期待されるレスポンスは2が除外され3,5となる。
    """
    todo_request_with_endpoint = databroker_api_repository.fetch_todo_requests('blue')
    assert set([r.id_ for r in todo_request_with_endpoint]) == set([request3_not_yet.id_, request5_failed_twice.id_])


def test_fetch_api_result_metadata_should_be_moved(psql_client, databroker_api_repository):
    """
    概要:
        datasetデータベースに未移動のbodyに関するApiResultMetadataのみが、
        きちんと取得されているのかを確認する

    取得される条件: 全てを同時に満たすもののみ
        - bodyがまだ存在している (bodyがNoneではない)
        - 成功したリクエスト (statusが200)

    登録するデータ:
        1. リクエスト未実行
        2. リクエスト失敗
        3. リクエスト成功、body未移動
        4. リクエスト成功、ただしbodyは移動済み
        5. リクエスト成功、body未移動（異なるエンドポイント）
        6. 1度目のリクエストは失敗、2度目のリクエスト成功、bodyは未移動

    テスト条件:
        1. 通常テスト。3,5,6のみが取得されればOK
        2. エンドポイントの指定。3,6のみが取得されればOK
    """
    # リクエスト群の作成
    request1_no_response = ApiRequest(
        endpoint='red',
        parameter={'param_a': 'value_a'},
        header={'header_a': 'value_a'},
        id_='20e70eec-fda5-db6f-bf52-3798108c2784',
        timestamp='2022-01-01 00:00:01'
    )
    request2_failed = ApiRequest(
        endpoint='red',
        parameter={'param_b': 'value_b'},
        header={'header_b': 'value_b'},
        id_='691fe01b-ba2a-efe1-3100-c2cac6fd8caa',
        timestamp='2022-01-01 00:00:02'
    )
    request3_success_body_not_moved = ApiRequest(
        endpoint='red',
        parameter={'param_c': 'value_c'},
        header={'header_c': 'value_c'},
        id_='7bf68cef-e69a-9fc9-0636-83d936340269',
        timestamp='2022-01-01 00:00:03'
    )
    request4_success_body_moved = ApiRequest(
        endpoint='red',
        parameter={'param_d': 'value_d'},
        header={'header_d': 'value_d'},
        id_='19ae2531-d78a-7553-86e5-74da1952deca',
        timestamp='2022-01-01 00:00:04'
    )
    request5_success_body_not_moved_another_endpoint = ApiRequest(
        endpoint='blue',
        parameter={'param_e': 'value_e'},
        header={'header_e': 'value_e'},
        id_='8bd09965-a92a-da89-46b4-2704c61df569',
        timestamp='2022-01-01 00:00:05'
    )
    request6_failed_success = ApiRequest(
        endpoint='red',
        parameter={'param_f': 'value_f'},
        header={'header_f': 'value_f'},
        id_='4cf8d655-fc85-bc17-3062-f15cc983f703',
        timestamp='2022-01-01 00:00:06'
    )
    # リクエスト群の登録
    databroker_api_repository.store_request(request1_no_response)
    databroker_api_repository.store_request(request2_failed)
    databroker_api_repository.store_request(request3_success_body_not_moved)
    databroker_api_repository.store_request(request4_success_body_moved)
    databroker_api_repository.store_request(request5_success_body_not_moved_another_endpoint)
    databroker_api_repository.store_request(request6_failed_success)
    # レスポンス群の作成
    response2_failed = ApiResponse(
        request_id=request2_failed.id_,
        status=400,
        header={'header_b': 'value_b'},
        body={'body_b': '一発失敗'},
        id_='f581c960-aee1-d73c-b5be-23b67a83a50e',
        timestamp='2022-01-02 00:01:00'
    )
    response3 = ApiResponse(
        request_id=request3_success_body_not_moved.id_,
        status=200,
        header={'header_c': 'value_c'},
        body={'body_c': '成功、未移動'},
        id_='17c5bc09-4e03-69f7-9b59-95941a05e459',
        timestamp='2022-01-02 00:02:00'
    )
    response4 = ApiResponse(
        request_id=request4_success_body_moved.id_,
        status=200,
        header={'header_d': 'value_d'},
        body=None,
        id_='0a5ec6b6-c799-9c42-9c2b-d16afa001617',
        timestamp='2022-01-02 00:03:00'
    )
    response5 = ApiResponse(
        request_id=request5_success_body_not_moved_another_endpoint.id_,
        status=200,
        header={'header_e': 'value_e'},
        body={'body_e': '成功、未移動'},
        id_='b80690e6-3f35-425d-306f-2c9c552db53e',
        timestamp='2022-01-02 00:04:00'
    )
    response6_first_failed = ApiResponse(
        request_id=request6_failed_success.id_,
        status=400,
        header={'header_f': 'value_f'},
        body={'body_f': '１度目失敗'},
        id_='034524d7-9c97-9931-c47f-175828b50997',
        timestamp='2022-01-02 00:05:00'
    )
    response6_second_success = ApiResponse(
        request_id=request6_failed_success.id_,
        status=200,
        header={'header_f': 'value_f'},
        body={'body_f': '２度目成功'},
        id_='65b574b6-e102-26b5-62e5-405b67a22d73',
        timestamp='2022-01-02 00:06:00'
    )
    # レスポンス群の登録
    databroker_api_repository.store_response(response2_failed)
    databroker_api_repository.store_response(response3)
    databroker_api_repository.store_response(response4)
    databroker_api_repository.store_response(response5)
    databroker_api_repository.store_response(response6_first_failed)
    databroker_api_repository.store_response(response6_second_success)
    # 通常テスト
    metadata = databroker_api_repository.fetch_api_result_metadata_should_be_moved()
    assert set([m.request_id for m in metadata]) == set(
        [
            request3_success_body_not_moved.id_, 
            request5_success_body_not_moved_another_endpoint.id_,
            request6_failed_success.id_
        ]
    )
    # エンドポイントを指定した場合のテスト
    metadata = databroker_api_repository.fetch_api_result_metadata_should_be_moved('red')
    assert set([m.request_id for m in metadata]) == set(
        [
            request3_success_body_not_moved.id_,
            request6_failed_success.id_
        ]
    )
