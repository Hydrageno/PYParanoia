function backHome(){
    /**
     * 功能：返回至主页面
     */
    window.location.href = './home.html';
}


function fetchGradewordbookQuestions(){
    /**
     * 用以获取不同年级不同时期的题目
     */
    // 首先需要获取用户的选择
    var gradePeriodRankSelectResult = document.getElementById('gradePeriodRankSelect').value;
    var hyperModeSelectResult = document.getElementById('hyperModeSelect').value;
    var settingToSend = {
        "mode": "gradewordbook",
        "gradeperiod": gradePeriodRankSelectResult,
        "hybrid_mode": hyperModeSelectResult
    };
    var settingJSON = JSON.stringify(settingToSend);
    // 使用 fetch 发送 POST 请求给服务器
    fetch('http://127.0.0.1:5000/fetch_questions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: settingJSON,
    })
    .then(response => response.json())
    .then(data => {
        var questionContainer = document.querySelector('.questions-container');
        var questions = data['questions'];
        console.log(questions)
        for(var i = 0; i < questions.length; i++)
        {
            var question = questions[i];
            var questionTemplate = document.createElement('div');
            questionTemplate.classList.add('question-template');
            questionTemplate.innerHTML = `
                第（<span class="question-id prefix">${question.question_id}</span>）题
                <br>
                <span class="prefix">题干</span>：
                <span class="question-maintext">${question.question_maintext}</span>
                <br>
                <span class="prefix">提示</span>：
                <span class="question-desc">${question.question_desc}</span>
                <br>
                <label for="q${question.question_id}"><span class="prefix">作答</span>：</label>
                <input type="text" class="question-reply" id="q${question.question_id}">
                <br>
                <br>
            `;
            questionContainer.appendChild(questionTemplate);
        }
    })
}


function fetchWordbookQuestions(){
    /**
     * 用以获取基于生字本的题目
     */
    var settingToSend = {
        "mode": "wordbook",
    };
    var settingJSON = JSON.stringify(settingToSend);
    // 使用 fetch 发送 POST 请求给服务器
    fetch('http://127.0.0.1:5000/fetch_questions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: settingJSON,
    })
    .then(response => response.json())
    .then(data => {
        var questionContainer = document.querySelector('.questions-container');
        var questions = data['questions'];
        console.log(questions)
        for(var i = 0; i < questions.length; i++)
        {
            var question = questions[i];
            var questionTemplate = document.createElement('div');
            questionTemplate.classList.add('question-template');
            questionTemplate.innerHTML = `
                第（<span class="question-id prefix">${question.question_id}</span>）题
                <br>
                <span class="prefix">题干</span>：
                <span class="question-maintext">${question.question_maintext}</span>
                <br>
                <span class="prefix">提示</span>：
                <span class="question-desc">${question.question_desc}</span>
                <br>
                <label for="q${question.question_id}"><span class="prefix">作答</span>：</label>
                <input type="text" class="question-reply" id="q${question.question_id}">
                <br>
                <br>
            `;
            questionContainer.appendChild(questionTemplate);
        }
    })
}