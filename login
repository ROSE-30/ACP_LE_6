<h2>Login</h2>
{# Heading for the login page #}

<form method="post">
    {# Hidden CSRF token for security to prevent malicious form submissions #}
    {{ form.hidden_tag() }}

    {# Username input field #}
    {{ form.username.label }}  {# Shows "Username" label #}
    {{ form.username() }}      {# Input box where user types their username #}
    <br>                        {# Line break for spacing #}

    {# Password input field #}
    {{ form.password.label }}  {# Shows "Password" label #}
    {{ form.password() }}      {# Input box for user password #}
    <br>                        {# Line break for spacing #}

    {# Submit button to log in #}
    {{ form.submit() }}        {# Button displays "Login" #}
</form>
