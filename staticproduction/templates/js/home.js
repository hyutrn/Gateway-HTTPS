const logout_element = document.querySelector('.Logout');
logout_element.addEventListener('click', logout);

const username_element = document.getElementById('Username');
username_element.innerHTML = getCookie('username');

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

function logout(e) {
    e.preventDefault();
    fetch('/sign_out', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            'Authorization': 'Token ' + getCookie('token')
        },
    }).then((response) => {
        if (response.status == 200) {
            document.cookie = "token=expired";
            window.location.href = "/login";
        }
        else {
            console.log(response);
        }
    });
}