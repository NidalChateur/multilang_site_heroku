// target : chabot/templates/chabot.html

let messages_list = document.getElementById("messagesList");
let form = document.getElementById("chatbotForm");
let input_message = document.getElementById("inputMessage");
let submit_button = document.getElementById("button-addon2");

form.addEventListener("submit", (event) => {
  //cancel refresh
  event.preventDefault();

  // check if input_message is not empty
  let message = input_message.value.trim();
  if (message.length === 0) {
    // return nothing to exit
    return;
  }

  // fill the message list with the user message
  messages_list.innerHTML += `    
    <li class="list-group-item list-group-item-secondary">
      <div class="message-sender"><b>You</b></div>
      <div class="message-content">${message}</div>
    </li>
    `;

  // reset input_message
  input_message.value = "";

  // disable the submit button
  submit_button.classList.value = "btn btn-outline-success disabled";

  // set fetch parameters

  //  empty because the post method is managed in this view
  let endpoint = "";

  options = {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      csrfmiddlewaretoken: document.querySelector("[name=csrfmiddlewaretoken]").value,
      message: message,
    }),
  };

  try {
    fetch(endpoint, options)
      .then((response) => response.json())
      .then((data) => {
        // get the openai response
        let chatbot_answer = data.response;

        // fill the message list with the chatbot answer
        messages_list.innerHTML += `    
        <li class="list-group-item list-group-item-success">
            <div class="message-sender"><b>AI Chatbot</b></div>
            <div class="message-content">${chatbot_answer}</div>
        </li>
        `;

        // enable submit button
        submit_button.classList.value = "btn btn-outline-success";
      });
  } catch (error) {
    console.error("Error fetching data :", error);
  }
});
