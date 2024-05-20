/***************************************************** Variables  ****************************************************/
const vacancy_vid = JSON.parse(document.getElementById('json-vacancy_vid').textContent)
const numDocuments = document.getElementById('numDocuments');
const btnStart = document.getElementById('btnStart');
let chatSocket =null;
const container = document.getElementById('default-chat-container');
const rows = document.querySelectorAll("table tbody tr");

const removeForm = ()=>{
    document.getElementById('formContainer').remove();
}

const alterTable = (data)=>{
    rows.forEach(row => {
        const link = row.querySelector("a");
        if (link) {
            const href = link.getAttribute('href');
            const match = data.find(item => href.includes(item.filename));
            if (match) {
                const compatibilityCell = row.querySelector('.compatibility');
                const summaryCell = row.querySelector('.summary');

                compatibilityCell.textContent = match.compatibility;
                summaryCell.textContent = match.summary;

                compatibilityCell.classList.add('alert-success');
                summaryCell.classList.add('alert-success');
            } else {
                row.remove();
            }
        }
    });
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
        try {
            if(data.type==='response')
            {
                removeForm();
                alterTable(data.data);
            }
        } 
        catch (error) 
        {
            console.error(error);
            alert("Error ao ler os dados dos Cvs");
        }
    }
        
    chatSocket.onclose = function() {
        console.log('Conexão fechada.');
        // window.alert("Conexão fechada");
    };
        
});
