function looksLikeUrl(value) {
    if (!value || value.length > 2048 || /\s/.test(value)) {
        return false;
    }

    var candidate = value;
    if (!/^[a-zA-Z][a-zA-Z0-9+.-]*:\/\//.test(candidate)) {
        candidate = "http://" + candidate;
    }

    try {
        var parsed = new URL(candidate);
        return Boolean(parsed.hostname && (parsed.hostname.includes(".") || parsed.hostname === "localhost"));
    } catch (error) {
        return false;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("scanForm");
    if (!form) {
        return;
    }

    var input = document.getElementById("url");
    var error = document.getElementById("urlError");
    var loading = document.getElementById("loadingBar");

    input.addEventListener("input", function () {
        input.classList.remove("is-invalid");
        error.classList.remove("show");
    });

    form.addEventListener("submit", function (event) {
        var value = input.value.trim();
        if (!looksLikeUrl(value)) {
            event.preventDefault();
            input.classList.add("is-invalid");
            error.classList.add("show");
            input.focus();
            return;
        }

        loading.classList.add("active");
        form.querySelector("button[type='submit']").disabled = true;
    });
});
