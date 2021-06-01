#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import asyncio


class CoroutineTask:

    def __init__(self):
        self.__lists = []
        self.__result = []
        self.__loop = asyncio.get_event_loop()

    def CreateCoroutine(self, coroutine, task_id):
        task = self.__loop.create_task(coroutine, name=task_id)
        self.__lists.append(task)

    def StartCoroutine(self):
        fut = asyncio.ensure_future(self.__main())
        self.__loop.run_until_complete(fut)
        try:
            pass
            # self.__loop.run_forever()
        except (KeyboardInterrupt, Exception):
            self.__loop.stop()

    async def __main(self):
        self.__result = await asyncio.gather(*self.__lists, return_exceptions=True)
        print(self.__result)

    def GetResult(self):
        return self.__result


async def test():
    print("Hello")
    return "Hello"
    await asyncio.sleep(1)


async def test2():
    print("World")
    return "World"
    await asyncio.sleep(1)


if __name__ == '__main__':
    c = CoroutineTask()
    c.CreateCoroutine(test(), "test")
    c.CreateCoroutine(test2(), "test2")
    c.StartCoroutine()
