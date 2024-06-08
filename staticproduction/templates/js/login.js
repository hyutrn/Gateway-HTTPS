
username = document.getElementById("username");
password = document.getElementById("password");

button = document.querySelector("button");

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

button.addEventListener("click", function (e) {
    e.preventDefault();
    button.setAttribute('disabled', '');
    button.innerHTML = "Logging in...";
    const csrftoken = getCookie('csrftoken');
    if (username.value == "" || password.value == "") {
        alert("Please enter both username and password");
    }
    else {
        // POST /login_page with parameters username and password
        // if successful, redirect to /home
        // else, alert("Invalid username or password")
        fetch('/login_page', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                console.log("successful login!");
                // Storage token in cookie for future requests
                document.cookie = "token=" + data.token;
                document.cookie = "username=" + data.user.username;
                window.location.href = "/home";
            }
            else if (data=="missing user") {
                alert("Wrong password");
            }
            else {
                alert("Invalid username");
            }
        });
    }
    button.removeAttribute('disabled');
    button.innerHTML = "Login";
});