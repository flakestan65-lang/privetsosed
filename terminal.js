import readline from 'readline';
import { execSync, spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import chalk from 'chalk';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: chalk.green('user@codesandbox:~$ ')
});

console.log(chalk.cyan('╔══════════════════════════════════════╗'));
console.log(chalk.cyan('║     🤖 AI Terminal v1.0              ║'));
console.log(chalk.cyan('║     Команды: help, ai, npm, etc     ║'));
console.log(chalk.cyan('╚══════════════════════════════════════╝'));
console.log('');

let currentDir = process.cwd();

function runCommand(cmd) {
  try {
    const result = execSync(cmd, { 
      cwd: currentDir,
      encoding: 'utf-8',
      stdio: 'pipe'
    });
    console.log(result);
  } catch (e) {
    console.log(chalk.red(e.message));
  }
}

rl.prompt();

rl.on('line', (line) => {
  const args = line.trim().split(' ');
  const command = args[0];
  const rest = args.slice(1).join(' ');

  switch(command) {
    case '':
      break;
      
    case 'help':
      console.log(chalk.yellow('Доступные команды:'));
      console.log('  help     - Эта справка');
      console.log('  ai       - Запустить ИИ-агента');
      console.log('  npm      - npm install <пакет>');
      console.log('  ls       - Список файлов');
      console.log('  cd       - Сменить директорию');
      console.log('  cat      - Показать файл');
      console.log('  mkdir    - Создать папку');
      console.log('  clear    - Очистить экран');
      console.log('  exec     - Выполнить shell команду');
      console.log('  python   - Запустить Python скрипт');
      break;

    case 'clear':
      console.clear();
      break;

    case 'ls':
      runCommand('ls -la');
      break;

    case 'cd':
      if (args[1]) {
        const newPath = path.resolve(currentDir, args[1]);
        if (fs.existsSync(newPath)) {
          currentDir = newPath;
          rl.setPrompt(chalk.green(`user@codesandbox:${path.basename(currentDir)}$ `));
        } else {
          console.log(chalk.red('Директория не найдена'));
        }
      }
      break;

    case 'cat':
      if (args[1]) {
        try {
          const content = fs.readFileSync(path.join(currentDir, args[1]), 'utf-8');
          console.log(content);
        } catch(e) {
          console.log(chalk.red('Файл не найден'));
        }
      }
      break;

    case 'mkdir':
      if (args[1]) {
        fs.mkdirSync(path.join(currentDir, args[1]), { recursive: true });
        console.log(chalk.green('Создано'));
      }
      break;

    case 'npm':
      console.log(chalk.blue('Выполняю npm...'));
      const npm = spawn('npm', rest.split(' '), { 
        cwd: currentDir,
        stdio: 'inherit'
      });
      npm.on('close', () => rl.prompt());
      return;

    case 'exec':
      if (rest) {
        console.log(chalk.blue(`$ ${rest}`));
        runCommand(rest);
      }
      break;

    case 'python':
      if (args[1]) {
        const py = spawn('python3', [args[1]], {
          cwd: currentDir,
          stdio: 'inherit'
        });
        py.on('close', () => rl.prompt());
        return;
      } else {
        console.log(chalk.red('Укажите файл: python script.py'));
      }
      break;

    case 'ai':
      console.log(chalk.magenta('🚀 Запуск ИИ-агента...'));
      const agent = spawn('node', ['ai-agent.js'], {
        cwd: currentDir,
        stdio: 'inherit'
      });
      agent.on('close', () => rl.prompt());
      return;

    default:
      // Пробуем выполнить как shell команду
      try {
        runCommand(line);
      } catch(e) {
        console.log(chalk.red(`Команда не найдена: ${command}`));
      }
  }

  rl.prompt();
});

rl.on('close', () => {
  console.log(chalk.yellow('\nДо свидания!'));
  process.exit(0);
});
