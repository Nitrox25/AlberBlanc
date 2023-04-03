import pytest
import json
import uuid
import random




@pytest.mark.asyncio
async def test_add_user(websocket_connection):
    async for ws in websocket_connection:
        payload = json.dumps(
            {
                "id": '2341514214' ,
                "method": "add",
                "name": 'Leo',
                "surname": 'Khanin',
                "phone": "+2128507",
                "age": 24
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


@pytest.mark.asyncio
@pytest.mark.parametrize("is_phone_duplicate, id , name, surname, age", [
    (False, str(uuid.uuid4()), "Chuck0", "Dorris0", 100500),  #
    (False, 7234, "Chuck1", "Dorris1", 100500),  #
    (False, str(uuid.uuid4()), 123, "Dorris3", 100500),  #
    (False, str(uuid.uuid4()), "Chuck2", 123, 100500),  #
    (False, str(uuid.uuid4()), "Chuck4", "Dorris4", "abc"),  #
    (False, str(uuid.uuid4()), None, "Dorris6", 100500),
    (False, str(uuid.uuid4()), "Chuck7", None, 100500),
    (False, str(uuid.uuid4()), "Chuck8", "Dorris9", None),
    (True, str(uuid.uuid4()), "Chuck9", "Dorris9", 100500),
    (True, str(uuid.uuid4()), 123, 456, "abc"),

])
async def test_add_user_param(websocket_connection, is_phone_duplicate, id, name, surname, age):
    async for ws in websocket_connection:
        unique_phone = f"+955{random.randint(100000, 999999)}" if not is_phone_duplicate else "+2128507"
        payload = json.dumps(
            {
                "id": id,
                "method": "add",
                "name": name,
                "surname": surname,
                "phone": unique_phone,
                "age": age
            }
        )
        await ws.send(payload)
        repl = await ws.recv()
        response = json.loads(repl)
        print(payload)
        print(response)
        assert response is not None
        assert response["method"] == "add"
        if not is_phone_duplicate:
            if isinstance(age, int):
                if isinstance(name, str) and isinstance(surname, str) and isinstance(id, str):
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
                    assert response['users'][0]['age'] == age
                    assert response['users'][0]['name'] == name
                    assert response['users'][0]['phone'] == unique_phone
                    assert response['users'][0]['surname'] == surname
                    # конец проверки
                elif isinstance(name, int) or isinstance(surname, int) and isinstance(id, int):
                    assert response["status"] == "failure"
                    assert response["reason"] == "[json.exception.type_error.302] type must be string, but is number"

                    # проверка что запись не появилось
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
                elif name is None or surname is None or id is None:
                    assert response["status"] == "failure"
                    assert response["reason"] == "[json.exception.type_error.302] type must be string, but is null"
                    # проверка что запись не появилось
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

            elif isinstance(age, str):
                assert response["status"] == "failure"
                assert response["reason"] == "[json.exception.type_error.302] type must be number, but is string"
                # проверка что запись не появилось
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

            elif age is None:
                assert response["status"] == "failure"
                assert response["reason"] == "[json.exception.type_error.302] type must be number, but is null"


        elif is_phone_duplicate:
            assert response["status"] == "failure"
            # проверка что запись не появилось
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
async def test_add_user_with_additional_par(websocket_connection):
    async for ws in websocket_connection:
        unique_phone = f"+955{random.randint(100000, 999999)}"
        payload = json.dumps(
            {
                "id": str(uuid.uuid4()),
                "method": "add",
                "name": "Test",
                "surname": "Test",
                "phone": unique_phone,
                "age": 27,
                "sex": "Male"
            }
        )
        await ws.send(payload)
        repl = await ws.recv()
        response = json.loads(repl)
        print(payload)
        print(response)
        assert response is not None
        assert response["method"] == "add"
        assert response["status"] == 'failure'
        # проверка того что пришло
        payload = json.dumps(
            {
                "id": f'{uuid.uuid4()}',
                "method": "select",
                "phone": unique_phone
            }
        )
        await ws.send(payload)
        repl = await ws.recv()
        response = json.loads(repl)
        print(payload)
        print(response)
