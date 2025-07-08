async function uploadImage() {
  const input = document.getElementById('imageInput');
  const file = input.files[0];
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch('/api/recognize', {
    method: 'POST',
    body: formData
  });
  const data = await res.json();
  displayResults(file, data.results);
}

async function enrollFace() {
  const fileInput = document.getElementById('enrollInput');
  const nameInput = document.getElementById('nameInput');
  const file = fileInput.files[0];
  const name = nameInput.value;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('name', name);

  const res = await fetch('/api/enroll', {
    method: 'POST',
    body: formData
  });

  const result = await res.json();
  alert(result.message);
}

function displayResults(file, results) {
  const reader = new FileReader();
  reader.onload = () => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.getElementById('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);

      results.forEach(face => {
        const [x, y, w, h] = face.box;
        ctx.strokeStyle = "#00FF00";
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, w, h);
        ctx.font = "16px Arial";
        ctx.fillStyle = "#00FF00";
        ctx.fillText(`${face.name} (${(face.confidence * 100).toFixed(1)}%)`, x, y - 5);
      });
    };
    img.src = reader.result;
  };
  reader.readAsDataURL(file);
}
