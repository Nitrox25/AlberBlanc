import pytest
import json
import uuid
import random


@pytest.mark.asyncio
@pytest.mark.parametrize("id , unique_phone",
                         [
                             (str(uuid.uuid4()), "+2128507"),  # значение из скрипта test1.py для проверки повторений
                             (str(uuid.uuid4()), 2128507),
                             (str(uuid.uuid4()), None)

                         ])
async def test_select_by_phone(websocket_connection, id, unique_phone):
    # add new for update
    async for ws in websocket_connection:
        payload = json.dumps(
            {
                "id": f'{id}',
                "method": "select",
                "phone": unique_phone
            }
        )
        await ws.send(payload)
        repl = await ws.recv()
        response = json.loads(repl)
        print(payload)
        print(response)
        if isinstance(unique_phone, str):
            assert response is not None
            assert response["method"] == "select"
            assert response["status"] == 'success'
            assert response['users'][0]['age'] == 100500
            assert response['users'][0]['name'] == 'Chuck'
            assert response['users'][0]['surname'] == 'Dorris'
            assert response['users'][0]['phone'] == unique_phone
        elif isinstance(unique_phone, int):
            assert response is not None
            assert response["method"] == "select"
            assert response['status'] == 'failure'
            assert response['reason'] == '[json.exception.type_error.302] type must be string, but is number'
        elif unique_phone is None:
            assert response is not None
            assert response["method"] == "select"
            assert response['status'] == 'failure'
            assert response['reason'] == '[json.exception.type_error.302] type must be string, but is null'


#

@pytest.mark.asyncio
@pytest.mark.parametrize("search_by_name, search_by_surname",
                         [
                             (True, False),
                             (False, True),
                             (False, False),  ## кейс который роняет приложение
                             (True, True)

                         ])
async def test_select_by_name(websocket_connection, search_by_name, search_by_surname):
    async for ws in websocket_connection:
        name = f"select_test_name_{random.randint(100000, 999999)}"
        surname = f"select_test_surname_{random.randint(100000, 999999)}"
        for i in range(5):
            unique_phone = f"+955{random.randint(100000, 999999)}"
            id = uuid.uuid4()
            payload = json.dumps(
                {
                    "id": f'{id}',
                    "method": "add",
                    "name": name,
                    "surname": surname,
                    "phone": unique_phone,
                    "age": 27
                }
            )
            await ws.send(payload)
            repl = await ws.recv()
            response = json.loads(repl)
            print(payload)
            print(response)
            assert response is not None
            assert response["method"] == "add"
            assert response["status"] == "success"
        if search_by_name and not search_by_surname:
            id = uuid.uuid4()
            payload = json.dumps(
                {
                    "id": f'{id}',
                    "method": "select",
                    "name": name
                }
            )
            await ws.send(payload)
            repl = await ws.recv()
            response = json.loads(repl)
            print(payload)
            print(response)
            assert response["method"] == "select"
            assert len(response['users']) == 5
            assert response["status"] == "success"
        elif search_by_surname and not search_by_name:
            id = uuid.uuid4()
            payload = json.dumps(
                {
                    "id": f'{id}',
                    "method": "select",
                    "surname": surname
                }
            )
            await ws.send(payload)
            repl = await ws.recv()
            response = json.loads(repl)
            print(payload)
            print(response)
            assert response["method"] == "select"
            assert len(response['users']) == 5
            assert response["status"] == "success"

        elif not search_by_surname and not search_by_name:
            id = uuid.uuid4()
            payload = json.dumps(
                {
                    "id": f'{id}',
                    "method": "select"
                }
            )
            await ws.send(payload)
            repl = await ws.recv()
            response = json.loads(repl)
            print(payload)
            print(response)

        elif search_by_surname and search_by_name:
            id = uuid.uuid4()
            payload = json.dumps(
                {
                    "id": f'{id}',
                    "method": "select",
                    "surname": surname,
                    "name": name

                }
            )
            await ws.send(payload)
            repl = await ws.recv()
            response = json.loads(repl)
            print(payload)
            print(response)
            assert response["method"] == "select"
            assert len(response['users']) == 5
            assert response["status"] == "success"
