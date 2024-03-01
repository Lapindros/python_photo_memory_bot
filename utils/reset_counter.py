import logging

import aiofiles as aiof


async def reset_counter():
    async with aiof.open("photo_counter.txt", "w") as out:
        await out.write(str(0))
        await out.flush()
        logging.info("Счетчик сброшен")
