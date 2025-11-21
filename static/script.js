function controlDevice(device, state) {
    fetch(`/api/control/${device}/${state}`, { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(`${device} ${state}:`, data);
        updateData();
    })
    .catch(error => {
        console.error('Erro ao controlar dispositivo:', error);
    });
}

// Função para atualizar os dados
function updateData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            window.location.reload();
        })
        .catch(error => {
            console.error('Erro ao atualizar dados:', error);
        });
}

//Responsável por atualizar as informações!
// Atualizar os dados a cada 5 segundos
setInterval(updateData, 5000);

document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.setAttribute('title', 'Clique para alterar o estado');
    });
});