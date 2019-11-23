const request = require('request');


let slider;
let textField;
let backToMenu;
let fileElem;

document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.slider');
    sessions_row = document.getElementById('sessions-row');
    textField = document.getElementById('text-field');
    backToMenu = document.getElementById('back-to-menu');
    fileElem = document.getElementById('fileElem');
    slider = instances = M.Slider.init(elems, {
        duration: 500,
        interval: 0,
        indicators: false
    })[0];
    slider.pause();
    backToMenu.addEventListener('click', () => {
        fileElem.value = null;
        slider.set(0);
        slider.pause();
    });
});

let dropArea = document.getElementById("drop-area");
dropArea.addEventListener('dragenter', handlerFunction, false)
dropArea.addEventListener('dragleave', handlerFunction, false)
dropArea.addEventListener('dragover', handlerFunction, false)
dropArea.addEventListener('drop', handlerFunction, false)

function handlerFunction() {}

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropArea.classList.add('highlight');
}

function unhighlight(e) {
    dropArea.classList.remove('highlight');
}

dropArea.addEventListener('drop', handleDrop, false)

function handleDrop(e) {
    let dt = e.dataTransfer
    let files = dt.files
    handleFiles(files)
}

function handleFiles(files) {
    if (files.length > 1) {
        alert('На данный момент поддерживается загрузка не более 1 файла :(');
        return;
    }
    uploadFile(files[0]);
}

function uploadFile(file) {
    console.log(file);
    if (file.type != "text/plain") {
        alert('Ты дебил? Я текст анализирую, нахер ты мне какую-то парашу тут суешь?! А ну быстро свалил с глаз моих и пока текстовый файл не притащишь, не возвращайся!');
        return;
    }
    let url = 'http://127.0.0.1:1337/api/analyze_file'
    let formData = new FormData();
    formData.append('file', file);
    fetch(url, {
            method: 'POST',
            body: formData
        })
        .then((res) => {
            res.json()
                .then((body) => {
                    data = body.data;
                    text = '<p>Оригинальный текст:</p>\n<p>';
                    changed_text = '<p>'
                    for (let [changed, new_word, old_word] of data) {
                        console.log(changed, new_word, old_word);
                        if (changed) {
                            text += `<mark title="${new_word}">${old_word}</mark> `;
                        } else {
                            text += old_word + ' ';
                        }
                        changed_text += new_word + ' ';
                    }
                    text += '</p>\n<br>\n<br>\n<br>\n'
                    text += '<p>Предлагаемый изменённый текст:</p>'
                    text += changed_text;
                    textField.innerHTML = text;
                    slider.set(1);
                    slider.pause();
                })
                .catch((e) => {
                    alert('Всё сломалось')
                });
        })
        .catch(() => {
            /* Ошибка. Информируем пользователя */
        });
}
