function clearFiles(inputName) {
    const input = document.querySelector(`input[type="file"][name="${inputName}"]`);
    if (input) input.value = '';
}