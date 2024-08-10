function form_validation()
{
    var email_id = document.getElementById('email_id');
    var password = document.getElementById('password');
    var cpassword = document.getElementById('cpassword');
    if (email_id.value.length == 0)
    {
        alert('email id is mandatory');
    }
    else if (password.value.length == 0)
    {
        alert('email id is mandatory');
    }
    else if (password.value.length <= 8 && password.value.length >= 15)
    {
        alert('password must be between 8 to 15 characters.');
    }
    else if (cpassword.value.length == 0)
    {
        alert('reenter your password in confirm password.');
    }
    if(password.value == cpassword.value)
    {
        return true;
    }
    else
    {
        document.getElementById('cpwd').innerText = "* Must be identical to password *";
    }
}

function formvalidation1():
{
    var number = document.getElementById('contact_no')
    if (number.value.length == 10)
    {
        return true;
    }
    else
    {
        document.getElementById('pwd').innerText = "* Please enter between 8 and 15 characters *";
        password.focus();
        return false;
    }
}

console.log('heyyyyyyyyyyyyyyyy');
const next_btn = document.getElementById('next');
next_btn.addEventListener('click', form_validation);