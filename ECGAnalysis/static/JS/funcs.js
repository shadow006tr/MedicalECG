
console.log("Hello");



if (window.FileList && window.File && window.FileReader)
{
    document.getElementById('file').addEventListener('change', event => {
        const file = event.target.files[0];
        console.log(file);
        const reader = new FileReader();
          reader.addEventListener('load', event => {
            console.log(event.target.result);
            document.getElementById('myVar').value = event.target.result;
            console.log(document.getElementById('myVar').value);
            variable = document.getElementById('myVar').value;
          });
          reader.readAsDataURL(file);
        });
}