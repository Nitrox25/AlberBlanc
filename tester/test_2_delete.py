import pytest
import json
import uuid
import random


@pytest.mark.asyncio
async def test_delete_user(websocket_connection):
    # add new for delete
    async for ws in websocket_connection:
        id = uuid.uuid4()
        unique_phone = f"+955{random.randint(100000, 999999)}"
        payload = json.dumps(
            {
                "id": f'{id}',
                "method": "add",
                "name": "Dell",
                "surname": 'Test',
                "phone": unique_phone,
                "age": 100500
            }
        )
        await ws.send(payload)
        repl = await ws.recv()
        response = json.loads(repl)
        print(payload)
        print(response)
        assert response is not None
        assert response["id"] is not None
        assert response["id"] == f'{id}'
        assert response["method"] == "add"
        assert response["status"] == "success"

        # проверка что запись появилась
        id = uuid.uuid4()
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
        assert response['users'][0]['age'] == 100500
        assert response['users'][0]['name'] == 'Dell'
        assert response['users'][0]['phone'] == unique_phone
        assert response['users'][0]['surname'] == 'Test'
        # конец проверки

        # delete user
        print("начало удаления")
        id = uuid.uuid4()
        payload = json.dumps(
            {
                "id": f'{id}',
                "method": "delete",
                "phone": unique_phone,
            }
        )
        await ws.send(payload)
        repl = await ws.recv()
        response = json.loads(repl)
        print(payload)
        print(response)
        assert response is not None
        assert response["id"] is not None
        assert response["id"] == f'{id}'
        assert response["method"] == "delete"
        assert response["status"] == "success"

        # Проверка что запись не осталась
        id = uuid.uuid4()
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
        assert response['method'] == 'select'
        assert response['status'] == 'failure'

        # конец проверки


@pytest.mark.asyncio
@pytest.mark.parametrize("id , phone_number",
                         [
                          (str(uuid.uuid4()), "+7111111"),
                          (str(uuid.uuid4()), 123),
                          (str(uuid.uuid4()), None)
                         ])
async def test_delete_user_param(websocket_connection, id, phone_number):
    async for ws in websocket_connection:

        # удаление пользака котрого нет - с валидным номером
        print("начало удаления")
        payload = json.dumps(
            {
                "id": id,
                "method": "delete",
                "phone": phone_number,
            }
        )
        await ws.send(payload)
        repl = await ws.recv()
        response = json.loads(repl)
        print(payload)
        print(response)
        assert response is not None
        assert response["id"] is not None
        assert response["id"] == f'{id}'
        assert response["method"] == "delete"
        if isinstance(phone_number, str):
            assert response["status"] == "failure"
            ## Проверка что запись не появилась
            id_for_check = uuid.uuid4()
            payload = json.dumps(
                {
                    "id": f'{id_for_check}',
                    "method": "select",
                    "phone": phone_number
                }
            )
            await ws.send(payload)
            repl = await ws.recv()
            response = json.loads(repl)
            print(payload)
            print(response)
            assert response['method'] == 'select'
            assert response['status'] == 'failure'
            ##   конец проверки

        elif isinstance(phone_number, int):
            assert response['reason'] == '[json.exception.type_error.302] type must be string, but is number'
            assert response["status"] == "failure"
            ## Проверка что запись не появилась
            id_for_check = uuid.uuid4()
            payload = json.dumps(
                {
                    "id": f'{id_for_check}',
                    "method": "select",
                    "phone": phone_number
                }
            )
            await ws.send(payload)
            repl = await ws.recv()
            response = json.loads(repl)
            print(payload)
            print(response)
            assert response['method'] == 'select'
            assert response['status'] == 'failure'
            ## конец проверки

        elif phone_number is None:
            assert response['reason'] == '[json.exception.type_error.302] type must be string, but is null'
            assert response["status"] == "failure"
            ## Проверка что запись не появилась
            id_for_check = uuid.uuid4()
            payload = json.dumps(
                {
                    "id": f'{id_for_check}',
                    "method": "select",
                    "phone": phone_number
                }
            )
            await ws.send(payload)
            repl = await ws.recv()
            response = json.loads(repl)
            print(payload)
            print(response)
            assert response['method'] == 'select'
            assert response['status'] == 'failure'
            ## конец проверки
