from bot_src.bot import task_bot

async def app(scope, receive, send):
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                await task_bot.start()
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                await task_bot.stop()
                await send({'type': 'lifespan.shutdown.complete'})
                break
    else:
        pass
