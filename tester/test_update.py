import pytest
import json
import uuid
import random


@pytest.mark.asyncio
@pytest.mark.parametrize('id , new_name , new_surname , new_age',
                         [
                             (str(uuid.uuid4()), "Update_name0", "Update_surname0", 27),
                             (str(uuid.uuid4()), "Update_name1", "Update_surname1", "abc"),
                             (str(uuid.uuid4()), "Update_name2", "Update_surname2", None),
                             (str(uuid.uuid4()), 123, "Update_surname4", 27),
                             (str(uuid.uuid4()), "Update_name5", 123, 27),
                             (str(uuid.uuid4()), "Update_name6", None, 27),
                             (str(uuid.uuid4()), None, "Update_surname7", 27)

                         ])
async def test_update_user_with_add(websocket_connection, id, new_name, new_surname, new_age):
    # add new for update
    async for ws in websocket_connection:
        id_for_check = uuid.uuid4()
        unique_phone = f"+955{random.randint(100000, 999999)}"
        payload = json.dumps(
            {
                "id": f'{id_for_check}',
                "method": "add",
                "name": "Update",
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
        assert response["method"] == "add"
        # проверка что новая запись появилась
        id_for_check = uuid.uuid4()
        payload = json.dumps(
            {
                "id": f'{id_for_check}',
                "method": "select",
                "phone": unique_phone
            }
        )
        await ws.send(payload)
        repl = await ws.recv()
        response = json.loads(repl)
        print(payload)
        print(response)
        assert response is not None
        assert response["method"] == "select"
        assert response['users'][0]['age'] == 100500
        assert response['users'][0]['name'] == 'Update'
        assert response['users'][0]['phone'] == unique_phone
        assert response['users'][0]['surname'] == 'Test'
        # конец проверки

        # update user
        print("начало обновления")
        if isinstance(new_age, int):
            if isinstance(new_name, str) and isinstance(new_surname, str):
                payload = json.dumps(
                    {
                        "id": id,
                        "method": "update",
                        "phone": unique_phone,
                        "name": new_name,
                        "surname": new_surname,
                        "age": new_age

                    }
                )
                await ws.send(payload)
                repl = await ws.recv()
                response = json.loads(repl)
                print(payload)
                print(response)
                assert response['method'] == 'update'
                assert response['status'] == 'success'
                # проверка обновления
                id_for_check = uuid.uuid4()
                payload = json.dumps(
                    {
                        "id": f'{id_for_check}',
                        "method": "select",
                        "phone": unique_phone
                    }
                )
                await ws.send(payload)
                repl = await ws.recv()
                response = json.loads(repl)
                print(payload)
                print(response)
                assert response is not None
                assert response["method"] == "select"
                assert response['users'][0]['age'] == new_age
                assert response['users'][0]['name'] == new_name
                assert response['users'][0]['phone'] == unique_phone
                assert response['users'][0]['surname'] == new_surname
                # конец проверки
            elif isinstance(new_name, int) or isinstance(new_surname, int):
                payload = json.dumps(
                    {
                        "id": id,
                        "method": "update",
                        "phone": unique_phone,
                        "name": new_name,
                        "surname": new_surname,
                        "age": new_age

                    }
                )
                await ws.send(payload)
                repl = await ws.recv()
                response = json.loads(repl)
                print(payload)
                print(response)
                assert response['method'] == 'update'
                assert response['status'] == 'failure'
                assert response['reason'] == '[json.exception.type_error.302] type must be string, but is number'
            elif new_name is None or new_surname is None:
                payload = json.dumps(
                    {
                        "id": id,
                        "method": "update",
                        "phone": unique_phone,
                        "name": new_name,
                        "surname": new_surname,
                        "age": new_age

                    }
                )
                await ws.send(payload)
                repl = await ws.recv()
                response = json.loads(repl)
                print(payload)
                print(response)
                assert response['method'] == 'update'
                assert response['status'] == 'failure'
                assert response['reason'] == '[json.exception.type_error.302] type must be string, but is null'

        elif isinstance(new_age, str):
            payload = json.dumps(
                {
                    "id": id,
                    "method": "update",
                    "phone": unique_phone,
                    "name": new_name,
                    "surname": new_surname,
                    "age": new_age

                }
            )
            await ws.send(payload)
            repl = await ws.recv()
            response = json.loads(repl)
            print(payload)
            print(response)
            assert response["status"] == "failure"
            assert response['reason'] == '[json.exception.type_error.302] type must be number, but is string'
        elif new_age is None:
            payload = json.dumps(
                {
                    "id": id,
                    "method": "update",
                    "phone": unique_phone,
                    "name": new_name,
                    "surname": new_surname,
                    "age": new_age

                }
            )
            await ws.send(payload)
            repl = await ws.recv()
            response = json.loads(repl)
            print(payload)
            print(response)
            assert response["status"] == "failure"
            assert response['reason'] == '[json.exception.type_error.302] type must be number, but is null'
