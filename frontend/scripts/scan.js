document.getElementById('imageInput').addEventListener('change', async function () {
    const plate = prompt("輸入偵測到的車牌號碼（暫代）");
    if (plate) {
        const response = await fetch('/api/check_plate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ plate: plate })
        });
        const data = await response.json();
        if (data.status === 'allowed') {
            document.getElementById('result').innerHTML = `<h2 style='color:green'>✅ 允許停放 (${data.owner_name})</h2>`;
        } else {
            document.getElementById('result').innerHTML = `<h2 style='color:red'>❌ 禁止停放</h2>`;
        }
    }
});
