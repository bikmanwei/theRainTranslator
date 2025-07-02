// 获取DOM元素
const textInput = document.getElementById('textInput');
const progressFill = document.getElementById('progressFill');
const charCount = document.getElementById('charCount');
const characterDisplay = document.getElementById('characterDisplay');

// 初始化空状态
function showEmptyState() {
    characterDisplay.innerHTML = '<div class="empty-state">Enjoy the rain!</div>';
}

// 调用后端API进行文本转换
async function translateText(inputText) {
    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: inputText })
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.output;
        } else {
            console.error('API错误:', data.error);
            return `错误: ${data.error}`;
        }
    } catch (error) {
        console.error('网络错误:', error);
        return '网络连接错误，请检查服务器是否运行';
    }
}

// 添加字符到显示区域
async function addCharacterToDisplay(text) {
    // 移除空状态
    const emptyState = characterDisplay.querySelector('.empty-state');
    if (emptyState) {
        emptyState.remove();
    }
    
    // 创建新的字符项（先显示加载状态）
    const characterItem = document.createElement('div');
    characterItem.className = 'character-item loading';
    
    // 添加时间戳
    const timestamp = new Date().toLocaleTimeString('en-US', {
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    
    characterItem.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; color: #FFFFFF;">Rain input: ${text}</span>
                <span style="font-size: 12px; color: #FFFFFF;">${timestamp}</span>
            </div>
            <div class="translation-result">
                <div class="loading-spinner">🌧️ Translating...</div>
            </div>
        </div>
    `;
    
    // 添加到显示区域顶部
    characterDisplay.insertBefore(characterItem, characterDisplay.firstChild);
    
    // 调用API获取翻译结果
    const translatedText = await translateText(text);
    
    // 更新显示结果
    const resultDiv = characterItem.querySelector('.translation-result');
    resultDiv.innerHTML = `<div class="translation-output">${translatedText}</div>`;
    characterItem.classList.remove('loading');
    
    // 限制显示的项目数量（最多显示10个）
    const items = characterDisplay.querySelectorAll('.character-item');
    if (items.length > 10) {
        items[items.length - 1].remove();
    }
}

// 更新进度条
function updateProgress(currentLength) {
    const percentage = (currentLength / 10) * 100;
    progressFill.style.width = percentage + '%';
    charCount.textContent = currentLength;
    
    // 如果达到最大长度，添加完成样式
    if (currentLength === 10) {
        progressFill.classList.add('complete');
        // 移除完成样式（为下次做准备）
        setTimeout(() => {
            progressFill.classList.remove('complete');
        }, 600);
    }
}

// 清空输入框和重置进度条
function resetInput() {
    textInput.value = '';
    updateProgress(0);
    textInput.focus(); // 重新聚焦到输入框
}

// 处理输入事件
textInput.addEventListener('input', function(e) {
    const currentLength = e.target.value.length;
    updateProgress(currentLength);
    
    // 当达到10个字符时
    if (currentLength === 10) {
        const inputText = e.target.value;
        
        // 延迟一下再显示和清空，让用户看到进度条满了
        setTimeout(() => {
            addCharacterToDisplay(inputText);
            resetInput();
        }, 300);
    }
});

// 处理键盘事件
textInput.addEventListener('keydown', function(e) {
    // 如果按下回车键且有内容，立即提交
    if (e.key === 'Enter' && e.target.value.trim().length > 0) {
        const inputText = e.target.value;
        addCharacterToDisplay(inputText);
        resetInput();
        e.preventDefault();
    }
});

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', function() {
    showEmptyState();
    textInput.focus(); // 自动聚焦到输入框
    
    // 添加一些示例提示
    setTimeout(() => {
        if (characterDisplay.querySelector('.empty-state')) {
            const hint = document.createElement('div');
            hint.style.cssText = `
                position: absolute;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 12px;
                opacity: 0;
                transition: opacity 0.3s ease;
                pointer-events: none;
                z-index: 1000;
            `;
            hint.textContent = '💡 After enter 10 characters, it will automatically convert to a poem, or press Enter to submit.';
            document.body.appendChild(hint);
            
            // 显示提示
            setTimeout(() => hint.style.opacity = '1', 100);
            
            // 5秒后隐藏提示
            setTimeout(() => {
                hint.style.opacity = '0';
                setTimeout(() => hint.remove(), 300);
            }, 5000);
        }
    }, 1000);
});

// 添加一些交互效果
textInput.addEventListener('focus', function() {
    this.parentElement.style.transform = 'scale(1.02)';
    this.parentElement.style.transition = 'transform 0.2s ease';
});

textInput.addEventListener('blur', function() {
    this.parentElement.style.transform = 'scale(1)';
});