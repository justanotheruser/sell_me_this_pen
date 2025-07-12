const socket = io("ws://localhost:8080");
//const socket = io("ws://sellmethispen.ru:80");

socket.on("message", (text) => {
  const el = document.createElement("li");
  el.innerHTML = text;
  document.querySelector("ul").appendChild(el);
});

document.getElementById("send").onclick = () => {
  const text_input = document.querySelector("input");
  try {
    socket.emit("message", text_input.value);
  } catch (err) {
    console.error(err);
  }
  text_input.value = "";
};
