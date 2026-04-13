import asyncio
import json
from pprint import pprint
import websockets

class OverleafWS:
    def __init__(self, cookies, host):
        self.cookies = cookies
        self.host = host
        self.ws = None
        self._joined = False

    async def connect(self, token: str, project_id: str):
        url = f"wss://www.{self.host}/socket.io/1/websocket/{token}?projectId={project_id}"

        cookie_str = "; ".join([f"{c.name}={c.value}" for c in self.cookies])
        headers = {
            "Cookie": cookie_str,
            "Origin": f"https://www.{self.host}",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
            ),
        }

        async with websockets.connect(
            url,
            additional_headers=headers,
            ping_interval=None,   # disable built-in ping, Socket.IO handles heartbeat
            ping_timeout=None,
        ) as ws:
            self.ws = ws
            print("WebSocket connected!")

            # Step 1: wait for server's "1::" connect confirmation
            first = await ws.recv()
            pprint(f"← {first}")
            # first should be "1::" — just acknowledge it, do NOT send it back

            # Step 2: emit joinProject immediately
            await self._emit(ws, "joinProject", {"project_id": project_id})

            # Step 3: listen forever
            await self._listen(ws, project_id)

    async def _emit(self, ws, event_name: str, *args):
        payload = json.dumps({"name": event_name, "args": list(args)})
        frame = f"5:::{payload}"
        pprint(f"→ [{event_name}] {frame}")
        await ws.send(frame)

    async def _listen(self, ws, project_id: str):
        async for message in ws:
            await self._handle_frame(ws, message, project_id)

    async def _handle_frame(self, ws, frame: str, project_id: str):
        pprint(f"← {frame}")

        # Socket.IO v0.9 frame: type:id:endpoint:data
        parts = frame.split(":", 3)
        msg_type = parts[0]

        match msg_type:
            case "2":
                # Heartbeat ping from server — must pong back
                await ws.send("2::")
                pprint("→ Pong")

            case "1":
                # Connect frame — server is confirming endpoint, do NOT reply
                pprint("   (endpoint connected, ignoring)")

            case "5":
                # Event
                if len(parts) == 4:
                    try:
                        data = json.loads(parts[3])
                        name = data.get("name", "")
                        args = data.get("args", [])
                        await self._dispatch(ws, name, args, project_id)
                    except json.JSONDecodeError as e:
                        pprint(f"JSON parse error: {e}")

            case "4":
                # Raw JSON message
                if len(parts) == 4:
                    pprint(f"📄 JSON msg: {parts[3]}")

            case "7":
                pprint(f"Server error: {frame}")

            case _:
                pprint(f"Unknown type {msg_type}")

    async def _dispatch(self, ws, event: str, args: list, project_id: str):
        match event:
            case "joinProjectResponse":
                if self._joined:
                    pprint("Duplicate joinProjectResponse ignored")
                    return
                self._joined = True
                project = args[0].get("project", {})
                pprint(f"Joined: {project.get('name')}")

                # Now join the root document
                root_doc_id = project.get("rootDoc_id")
                if root_doc_id:
                    await self.join_doc(ws, root_doc_id)

            case "joinDocResponse":
                pprint(f"Doc content received: {args}")

            case "otUpdateApplied":
                pprint(f"OT update: {args}")

            case "broadcastDocMeta":
                pprint(f"Doc meta: {args}")

            case _:
                pprint(f"[{event}]: {args}")

    async def join_doc(self, ws, doc_id: str):
        """Join a document to get its content and receive live updates."""
        await self._emit(ws, "joinDoc", doc_id, {"encodeRanges": True})
        pprint(f"→ joinDoc sent for {doc_id}")
