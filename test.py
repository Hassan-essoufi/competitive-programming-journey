import asyncio

async def hello():
    print('Hello')
    await asyncio.sleep(1)  # Wait for one second before printing 'world'
    print('World')

# Run the coroutine in an event loop
asyncio.run(hello())