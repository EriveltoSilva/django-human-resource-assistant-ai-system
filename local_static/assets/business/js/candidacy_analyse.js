/***************************************************** Variables  ****************************************************/
// const chatInput = document.querySelector("#chat-input");
// const sendButton = document.querySelector("#send-btn");
// const chatContainer = document.querySelector(".chat-container");
// const themeButton = document.querySelector("#theme-btn");
// const deleteButton = document.querySelector("#delete-btn");
// const initialInputHeight = chatInput.scrollHeight;


const vacancy_vid = JSON.parse(document.getElementById('json-vacancy_vid').textContent)
const numDocuments = document.getElementById('numDocuments');
const btnStart = document.getElementById('btnStart');
let chatSocket =null;
const container = document.getElementById('default-chat-container');


const createAlert = (text)=>{
    let p = document.createElement('p');
    p.innertHTML = ""
    p.className = 'alert alert-success';
    p.textContent = text;
    return p;
}
btnStart.addEventListener('click', () => {
    if(!numDocuments.value)
        {
            alert("Preencha o número de documentos que devem ser retornados!");
            return;
        }
        
        chatSocket = new WebSocket(`ws://${window.location.host}/ws/analisar-candidaturas/${vacancy_vid}/${numDocuments.value}/`);
        
        chatSocket.onopen = function(e) {
            console.log('Conexão estabelecida.');
            // window.alert('Conexão estabelecida.');

            let child = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Processando...
            `;
            btnStart.innerHTML=``;
            btnStart.setAttribute('disabled', true);
            btnStart.insertAdjacentHTML('beforeend', child);
            chatSocket.send(JSON.stringify({"message": "data"}))
        };
        
        
        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data)
            console.log("Data Received:", data);

            if(data.type==='response')
            {
                container.innerHTML = "";
                const child=`
                    <p class="alert alert-success">
                        Os Dados chegaram
                    </p>
                `;
                container.insertAdjacentHTML('beforeend', child);
            }
        }
        
        chatSocket.onclose = function() {
            console.log('Conexão fechada.');
            // window.alert("Conexão fechada");
        };
        
    });

// chatSocket.send(JSON.stringify({"message": userText, "room_name":chatID, "username":username}))

// let userText = null;
// let chatResponseElement = null;

/***************************************************** FunctionS  ****************************************************/
// const clearInput = () => {
    //     chatInput.value = "";
//     chatInput.style.height = `${initialInputHeight}px`;
// }

// const copyResponse = (copyBtn) => {
//     const reponseTextElement = copyBtn.parentElement.querySelector("p");
//     navigator.clipboard.writeText(reponseTextElement.textContent);
//     copyBtn.textContent = "done";
//     setTimeout(() => copyBtn.textContent = "content_copy", 1000);
// }

// const createChatElement = (content, className) => {
//     const chatDiv = document.createElement("div");
//     chatDiv.classList.add("chat", className);
//     chatDiv.innerHTML = content;
//     return chatDiv;
// }

// const loadDataFromLocalstorage = () => {
//     document.body.classList.toggle("light-mode", localStorage.getItem("themeColor") === "light_mode");
//     if (localStorage.getItem("all-chats"))
//         chatContainer.innerHTML = localStorage.getItem("all-chats");
//     chatContainer.scrollTo(0, chatContainer.scrollHeight); // Scroll to bottom of the chat container
// }

// const showTypingAnimation = () => {
//     const html = `<div class="chat-content">
//     <div class="chat-details">
//     <img src="/static/assets/images/chatbot.png" alt="chatbot-img">
//     <div class="typing-animation">
//     <div class="typing-dot" style="--delay: 0.2s"></div>
//     <div class="typing-dot" style="--delay: 0.3s"></div>
//     <div class="typing-dot" style="--delay: 0.4s"></div>
//     </div>
//     </div>
//     <span onclick="copyResponse(this)"><i class="bi bi-copy"></i></span>
//     </div>`;
//     const incomingChatDiv = createChatElement(html, "incoming");
//     chatContainer.appendChild(incomingChatDiv);
//     chatContainer.scrollTo(0, chatContainer.scrollHeight);
//     chatResponseElement = incomingChatDiv;
//     // getChatResponse(incomingChatDiv);
// }

// const handleOutgoingChat = () => {
//     userText = chatInput.value.trim();
//     if (!userText) return;

//     clearInput();

//     const html = `<div class="chat-content">
//     <div class="chat-details">
//     <img src="/static/assets/images/user.png" alt="user-img">
//     <p>${userText}</p>
//     </div>
//     </div>`;

//     const outgoingChatDiv = createChatElement(html, "outgoing");
//     chatContainer.querySelector(".default-text")?.remove();
//     chatContainer.appendChild(outgoingChatDiv);
//     chatContainer.scrollTo(0, chatContainer.scrollHeight);

//     chatSocket.send(JSON.stringify({"message": userText, "room_name":roomName, "username":username}))
//     showTypingAnimation();
// }

// const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat-pdf/${username}/${roomName}/`);


// chatSocket.onmessage = function (e) {
    // const pElement = document.createElement("p");
    // const data = JSON.parse(e.data)
    
    // console.log("Data:", data);
    // if (data.type == 'response') 
    // {
    //     pElement.textContent = data.message;
    //     console.log(data.message);
    // }
    // else{
    //     pElement.classList.add("error");
    //     pElement.textContent = "Oops! Something went wrong while retrieving the response. Please try again.";
    // }
    // const incomingChatDiv = chatResponseElement;
    // incomingChatDiv.querySelector(".typing-animation").remove();
    // incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
    // localStorage.setItem("all-chats", chatContainer.innerHTML);
    // chatContainer.scrollTo(0, chatContainer.scrollHeight);
    // chatInput.focus();
// }

// chatSocket.onclose = function() {
//     console.log('Conexão fechada.');
//     // window.alert("Conexão fechada");
// };

/***************************************************** Events  ****************************************************/
// sendButton.addEventListener("click", handleOutgoingChat);

// themeButton.addEventListener("click", () => {
//     document.body.classList.toggle("light-mode");
//     localStorage.setItem("themeColor", themeButton.innerText);
// });


// chatInput.addEventListener("input", () => {
//     chatInput.style.height = `${initialInputHeight}px`;
//     chatInput.style.height = `${chatInput.scrollHeight}px`;
// });

// chatInput.addEventListener("keydown", (e) => {
//     if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
//         e.preventDefault();
//         handleOutgoingChat();
//     }
// });


// deleteButton.addEventListener("click", () => {
//     if (confirm("Tem a certeza de que deseja eliminar toda a conversa?")) 
//     {
//         localStorage.removeItem("all-chats");
//         loadDataFromLocalstorage();
//         clearInput();
//     }
// });

// loadDataFromLocalstorage();

// window.addEventListener("load", ()=>{
    // chatContainer.querySelector(".default-text")?.remove();
// })