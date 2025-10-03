export function createWS(onMessage){
  const ws = new WebSocket("ws://localhost:8000/ws/telemetry");
  ws.onopen = () => console.log("WS open");
  ws.onmessage = (ev) => {
    const data = JSON.parse(ev.data);
    onMessage(data);
  };
  ws.onclose = () => console.log("WS closed");
  return ws;
}
