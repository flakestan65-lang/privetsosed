import readline from 'readline';
import chalk from 'chalk';
import ora from 'ora';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Здесь подключи свой API ключ
const OPENAI_API_KEY = process.env.OPENAI_API_KEY || 'your-key-here';

console.log(chalk.magenta('╔══════════════════════════════════════╗'));
console.log(chalk.magenta('║     🤖 AI Агент v1.0                 ║'));
console.log(chalk.magenta('║     Режимы: chat, code, shell       ║'));
console.log(chalk.magenta('╚══════════════════════════════════════╝'));
console.log('');

const modes = {
  chat: 'Обычный диалог',
  code: 'Помощь с кодом',
  shell: 'Генерация команд'
};

let currentMode = 'chat';

function askQuestion() {
  rl.question(chalk.cyan(`[${currentMode}] > `), async (input) => {
    if (input.toLowerCase() === 'exit') {
      console.log(chalk.yellow('ИИ-агент завершен'));
      rl.close();
      return;
    }

    if (input.startsWith('/mode ')) {
      const newMode = input.split(' ')[1];
      if (modes[newMode]) {
        currentMode = newMode;
        console.log(chalk.green(`Режим изменен: ${modes[newMode]}`));
      } else {
        console.log(chalk.red('Доступные режимы: chat, code, shell'));
      }
      askQuestion();
      return;
    }

    if (input.startsWith('/help')) {
      console.log(chalk.yellow('Команды:'));
      console.log('  /mode chat  - Диалог');
      console.log('  /mode code  - Помощь с кодом');
      console.log('  /mode shell - Генерация команд');
      console.log('  exit        - Выход');
      askQuestion();
      return;
    }

    const spinner = ora('Думаю...').start();

    try {
      // Здесь реальный запрос к API
      // Для демо — эмуляция ответа
      await new Promise(r => setTimeout(r, 1500));
      spinner.stop();

      const responses = {
        chat: `Ответ на "${input}": Это демо-ответ. Добавь реальный API ключ для работы с OpenAI.`,
        code: `// Код для: ${input}\nfunction example() {\n  console.log("Hello World");\n}`,
        shell: `# Команда для: ${input}\necho "Выполняю задачу..."\nls -la`
      };

      console.log(chalk.white(responses[currentMode]));
      
    } catch (e) {
      spinner.stop();
      console.log(chalk.red('Ошибка: ' + e.message));
    }

    askQuestion();
  });
}

askQuestion();
