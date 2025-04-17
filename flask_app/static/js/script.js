// Обновленный код функции loadStatistics
async function loadStatistics() {
    try {
        const response = await fetch('/statistic');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log("Fetched Data:", data);

        // График пользователей
        createUserGraph(data.user_data);
        createPostGraph(data.post_data);

        // Обновление списков значений
        updateUserStats(data.user_data);
        updatePostStats(data.post_data);

    } catch (error) {
        console.error("Failed to load data:", error);
    }
}

function updateUserStats(userData) {
    const userStatsList = document.getElementById('user-stats');
    userStatsList.innerHTML = `
        <li>Logged Users: ${userData.logged_users[userData.logged_users.length - 1]}</li>
        <li>Visitors: ${userData.visitors[userData.visitors.length - 1]}</li>
        <li>Unique Visitors: ${userData.unique_visitors[userData.unique_visitors.length - 1]}</li>
        <li>Sent Emails: ${userData.sent_emails[userData.sent_emails.length - 1]}</li>
    `;
}

function updatePostStats(postData) {
    const postStatsList = document.getElementById('post-stats');
    postStatsList.innerHTML = `
        <li>Posts: ${postData.posts[postData.posts.length - 1]}</li>
        <li>Topics: ${postData.topics[postData.topics.length - 1]}</li>
    `;
}