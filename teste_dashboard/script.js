document.addEventListener('DOMContentLoaded', function () {
    fetch('https://dados.saude.go.gov.br/api/3/action/datastore_search?resource_id=5a4b5bbe-98c6-4d7c-8aed-d5de162dc605&limit=13000')
        .then(response => response.json())
        .then(data => {
            const chartData = processData(data.result.records);
            createCharts(chartData);
        });

    function processData(records) {
        // Processar os dados conforme necessário
        return records;
    }

    function createCharts(data) {
        const chartContainer = document.getElementById('charts-container');

        // Exemplo de criação de um gráfico
        const chartDiv = document.createElement('div');
        chartDiv.style.width = '600px';
        chartDiv.style.height = '400px';
        chartContainer.appendChild(chartDiv);

        const chart = echarts.init(chartDiv);
        const option = {
            title: {
                text: 'Exemplo de Gráfico'
            },
            tooltip: {},
            xAxis: {
                data: data.map(item => item.nome)
            },
            yAxis: {},
            series: [{
                type: 'bar',
                data: data.map(item => item.valor)
            }]
        };
        chart.setOption(option);
    }
});
