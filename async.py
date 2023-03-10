import asyncio, time
from aiohttp import ClientSession
from more_itertools import chunked
from db import Person, Session, engine, Base
CHUNK_SIZE = 10


async def get_url(url, session, name):
    start_get_url = time.monotonic()
    print(f'get_url start {url}')
    async with session.get(url) as response:
        response_json = await response.json()
        print(f'get_url finish {url} {time.monotonic()-start_get_url}')
        return response_json[name]


async def get_people(people_id, ClientSession, sep_dict):
    start_get_people = time.monotonic()
    print(f'get people start {people_id}')
    async with ClientSession as session:
        response = await session.get(f'https://swapi.dev/api/people/{people_id}')
        response_json = await response.json()

        try:
            for key, item in sep_dict.items():
                response_json[key] = ', '.join(
                    await asyncio.gather(*(get_url(url, session, item) for url in response_json[key])))
            response_json['id'] = people_id
            print(f'get_people finish {people_id} {time.monotonic() - start_get_people}')
            return response_json
        except:
            pass


async def insert_people(people_chunk):
    start_insert = time.monotonic()
    print(f'insert_people start')
    persons = [Person(pers_id=int(i['id']),
                      birth_year=i['birth_year'],
                      films=i['films'],
                      gender=i['gender'],
                      hair_color=i['hair_color'],
                      height=i['height'],
                      homeworld=i['homeworld'],
                      mass=i['mass'],
                      name=i['name'],
                      species=i['species'],
                      starships=i['starships'],
                      vehicles=i['vehicles']
                      ) for i in people_chunk if i]
    async with Session() as session:
        session.add_all(persons)
        await session.commit()
        print(f'insert_people finish {time.monotonic() - start_insert}')


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    sep_dict = {'species': 'name', 'films': 'title', 'starships': 'name', 'vehicles': 'name'}
    coro = (get_people(i, ClientSession(), sep_dict) for i in range(1, 84))
    for coros_chunk in chunked(coro, CHUNK_SIZE):
        asyncio.create_task(insert_people(await asyncio.gather(*coros_chunk)))
    tasks = set(asyncio.all_tasks()) - {asyncio.current_task()}
    for task in tasks:
        await task


start = time.monotonic()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
print(f'total time spent: {time.monotonic() - start}')
