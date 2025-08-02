document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('login-button');
    const scenarioButtons = document.querySelectorAll('.scenario-btn');
    const scenarioParams = document.getElementById('scenario-params');
    const executeScenarioButton = document.getElementById('execute-scenario');

    loginButton.addEventListener('click', function() {
        // 登录系统的逻辑
        console.log('登录系统');
    });

    scenarioButtons.forEach(button => {
        button.addEventListener('click', function() {
            const scenario = this.getAttribute('data-scenario');
            if (scenario === 'd') {
                scenarioParams.style.display = 'block';
                executeScenarioButton.style.display = 'block';
            } else {
                scenarioParams.style.display = 'none';
                executeScenarioButton.style.display = 'none';
            }
            scenarioButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });
});