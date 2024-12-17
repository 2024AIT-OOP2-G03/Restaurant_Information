// HTMLで渡されたPythonのデータを利用
const labels = indexData.map(item => item.menuName); // 商品名のリスト
const data = indexData.map(item => item.sumPrice);   // 各商品の合計金額

// 棒グラフを描画
const ctx = document.getElementById('barChart').getContext('2d');
const barChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: '売上高 (円)',
            data: data,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
