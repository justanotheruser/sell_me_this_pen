const socket = io("ws://localhost:8080");
//const socket = io("ws://sellmethispen.ru:80");

function add_message_to_dialog(text) {
  const el = document.createElement("li");
  el.innerHTML = text;
  document.querySelector("ul").appendChild(el);
}

socket.on("message", (text) => {
  const el = document.createElement("li");
  el.innerHTML = text;
  document.querySelector("ul").appendChild(el);
});

send_btn = document.getElementById("send");
send_btn.onclick = () => {
  const text_input = document.querySelector("textarea");
  add_message_to_dialog(text_input.value)
  try {
    socket.emit("message", text_input.value);
  } catch (err) {
    console.error(err);
  }
  text_input.value = "";
};

send_btn.addEventListener("keyup", function (event) {
  event.preventDefault();
  if (event.keyCode === 13) {
    document.getElementById("send").click();
  }
});
