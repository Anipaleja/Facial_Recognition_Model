const dropzone = document.getElementById('dropzone');
const imageInput = document.getElementById('imageInput');
const loading = document.getElementById('loading');

dropzone.addEventListener('click', () => imageInput.click());
dropzone.addEventListener('dragover', e => {
  e.preventDefault();
  dropzone.classList.add('hover');
});
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('hover'));
dropzone.addEventListener('drop', e => {
  e.preventDefault();
  dropzone.classList.remove('hover');
  imageInput.files = e.dataTransfer.files;
});

document.getElementById('themeToggle').onclick = () => {
  const html = document.documentElement;
  const dark = html.getAttribute('data-theme') === 'dark';
  html.setAttribute('data-theme', dark ? 'light' : 'dark');
};

async function uploadImage() {
  const file = imageInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  loading.style.display = 'block';
  const res = await fetch('/api/recognize', {
    method: 'POST',
    body: formData
  });
  const data = await res.json();
  loading.style.display = 'none';
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

  loading.style.display = 'block';
  const res = await fetch('/api/enroll', {
    method: 'POST',
    body: formData
  });
  loading.style.display = 'none';

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
function toggleTheme() {
    document.body.classList.toggle("dark");
}

document.addEventListener("DOMContentLoaded", () => {
    const loader = document.getElementById("loader");
    if (loader) {
        loader.style.display = "none";
    }

    const webcamBtn = document.getElementById("webcam-btn");
    if (webcamBtn) {
        webcamBtn.addEventListener("click", () => {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    const video = document.getElementById("webcam");
                    video.srcObject = stream;
                    video.play();
                })
                .catch(console.error);
        });
    }
});
