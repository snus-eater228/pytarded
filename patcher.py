#!/usr/bin/env python3
"""
Patcher для визуальной новеллы pytarded.

Использование:
    python patcher.py                    # Патчит все .rpy файлы из unpatched/ в game/
    python patcher.py -f script.rpy      # Патчит только script.rpy
    python patcher.py -f chapter1.rpy    # Патчит только chapter1.rpy
    python patcher.py --interval 10      # Меняет интервал (по умолчанию 5)
    python patcher.py --dry-run          # Показывает что будет сделано, но не записывает
"""

import argparse
import re
import shutil
from pathlib import Path

# Настройки по умолчанию
UNPATCHED_DIR = Path("unpatched")
GAME_DIR = Path("game")
CHECKPOINT_INTERVAL = 5  # Каждые N строк прогресса вставляем метку

# Что считается "строкой прогресса"
def is_progress_line(line: str) -> bool:
    """
    Определяет, является ли строка строкой прогресса сценария.
    Возвращает True для диалогов, меню, выборов, лейблов.
    """
    stripped = line.strip()
    
    # Пустые строки и комментарии — не считаем
    if not stripped or stripped.startswith('#'):
        return False
    
    # Диалог: имя персонажа + кавычки
    # Примеры: lars "Привет!", dave happy "Текст", narrator "Рассказ"
    if re.match(r'^[a-zA-Zа-яА-ЯёЁ_]+\s+"', stripped):
        return True
    
    # Диалог рассказчика (просто кавычки в начале)
    if stripped.startswith('"'):
        return True
    
    # Меню
    if stripped.startswith('menu:'):
        return True
    
    # Лейблы и прыжки (тоже прогресс)
    if stripped.startswith('label ') or stripped.startswith('jump '):
        return True
    
    # Выборы внутри menu (отступ + кавычки + двоеточие)
    # Пример: "    \"Взять ключ\":\n"
    if stripped.startswith('"') and ':' in stripped:
        return True
    
    if stripped.startswith('$'):
        return False
    
    return False


def patch_file(input_path: Path, output_path: Path, interval: int, dry_run: bool = False) -> dict:
    """
    Патчит один .rpy файл, вставляя checkpoint-метки каждые `interval` строк прогресса.
    Метки НЕ вставляются внутри блока menu: — только перед ним.
    Отступ меток соответствует отступу окружающих строк.
    """
    if not input_path.exists():
        return {'error': f'Файл не найден: {input_path}'}
    
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Проверяем, не пропатчен ли уже исходник
    if any('.cp_' in line for line in lines):
        return {'skipped': True, 'reason': 'Исходник уже содержит .cp_ метки'}
    
    new_lines = []
    current_label = None
    progress_count = 0
    cp_counter = 0
    checkpoints_inserted = 0
    
    in_menu_block = False
    menu_indent = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Отслеживаем текущий label
        label_match = re.match(r'^label\s+(\w+):', stripped)
        if label_match:
            current_label = label_match.group(1)
            cp_counter = 0
            progress_count = 0
            in_menu_block = False
            menu_indent = 0
        
        # Проверяем, вышли ли мы из блока menu
        if in_menu_block and stripped and not stripped.startswith('#'):
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= menu_indent:
                in_menu_block = False
        
        # Проверяем, вошли ли мы в блок menu
        if stripped.startswith('menu:'):
            in_menu_block = True
            menu_indent = len(line) - len(line.lstrip())
        
        # Считаем строки прогресса внутри label
        if current_label and is_progress_line(line):
            progress_count += 1
            
            # Если мы внутри блока menu или текущая строка — это menu:,
            # пропускаем вставку метки
            if in_menu_block or stripped.startswith('menu:'):
                new_lines.append(line)
                continue
            
            # Каждые `interval` строк вставляем checkpoint-метку
            if progress_count % interval == 0:
                cp_counter += 1
                cp_name = f"{current_label}.cp_{cp_counter}"
                
                # ИСПРАВЛЕНИЕ: берем отступ от ТЕКУЩЕЙ строки, а не от следующей
                current_indent = len(line) - len(line.lstrip())
                indent_str = ' ' * current_indent
                
                # Вставляем checkpoint-блок с правильным отступом
                new_lines.append(f"{indent_str}# === CHECKPOINT: {cp_name} ===\n")
                new_lines.append(f"{indent_str}label {cp_name}:\n")
                new_lines.append(f"{indent_str}    pass\n")
                new_lines.append(f"{indent_str}    # Продолжение сценария...\n")
                # НЕ добавляем пустую строку — она может сломать отступы
                checkpoints_inserted += 1
        
        new_lines.append(line)
    
    stats = {
        'lines': len(lines),
        'progress_lines': progress_count,
        'checkpoints': checkpoints_inserted
    }
    
    if dry_run:
        return stats
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return stats
def main():
    parser = argparse.ArgumentParser(
        description='Patcher для визуальной новеллы pytarded. '
                    'Вставляет checkpoint-метки в .rpy файлы.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  python patcher.py                      # Патчит все файлы из unpatched/ в game/
  python patcher.py -f script.rpy        # Патчит только script.rpy
  python patcher.py -f chapter1.rpy -i 10  # Интервал 10 строк
  python patcher.py --dry-run            # Предварительный просмотр
        """
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Конкретный файл для патчинга (из папки unpatched/)'
    )
    parser.add_argument(
        '-i', '--interval',
        type=int,
        default=CHECKPOINT_INTERVAL,
        help=f'Интервал checkpoint-меток (по умолчанию {CHECKPOINT_INTERVAL})'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Показать что будет сделано, но не записывать файлы'
    )
    parser.add_argument(
        '--unpatched',
        type=Path,
        default=UNPATCHED_DIR,
        help=f'Папка с оригиналами (по умолчанию {UNPATCHED_DIR})'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=GAME_DIR,
        help=f'Папка для пропатченных файлов (по умолчанию {GAME_DIR})'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print(" PATCHER для pytarded")
    print("=" * 70)
    print(f"Исходники: {args.unpatched}")
    print(f"Вывод:     {args.output}")
    print(f"Интервал:  {args.interval} строк прогресса")
    print(f"Dry run:   {args.dry_run}")
    print("=" * 70)
    
    # Определяем список файлов для патчинга
    if args.file:
        files_to_patch = [args.unpatched / args.file]
    else:
        files_to_patch = sorted(args.unpatched.glob("*.rpy"))
    
    if not files_to_patch:
        print(f"❌ Файлы не найдены в {args.unpatched}")
        return
    
    total_stats = {
        'files': 0,
        'lines': 0,
        'progress_lines': 0,
        'checkpoints': 0,
        'skipped': 0
    }
    
    for input_path in files_to_patch:
        if not input_path.exists():
            print(f"❌ Не найден: {input_path}")
            continue
        
        output_path = args.output / input_path.name
        relative_name = input_path.name
        
        print(f"\n📄 {relative_name}")
        
        stats = patch_file(input_path, output_path, args.interval, args.dry_run)
        
        if 'error' in stats:
            print(f"   ❌ {stats['error']}")
            continue
        
        if stats.get('skipped'):
            print(f"   ⚠️  Пропущен: {stats.get('reason', 'неизвестно')}")
            total_stats['skipped'] += 1
            continue
        
        total_stats['files'] += 1
        total_stats['lines'] += stats['lines']
        total_stats['progress_lines'] += stats['progress_lines']
        total_stats['checkpoints'] += stats['checkpoints']
        
        print(f"   ✅ Строк: {stats['lines']}")
        print(f"   📊 Прогресс-строк: {stats['progress_lines']}")
        print(f"   🎯 Вставлено меток: {stats['checkpoints']}")
        
        if not args.dry_run:
            print(f"   💾 Записано в: {output_path}")
    
    print("\n" + "=" * 70)
    print("📊 ИТОГО:")
    print(f"   Файлов обработано: {total_stats['files']}")
    print(f"   Всего строк: {total_stats['lines']}")
    print(f"   Прогресс-строк: {total_stats['progress_lines']}")
    print(f"   Вставлено меток: {total_stats['checkpoints']}")
    if total_stats['skipped']:
        print(f"   Пропущено: {total_stats['skipped']}")
    print("=" * 70)
    
    if args.dry_run:
        print("\n️  Это был dry-run. Файлы не были изменены.")
        print("   Запустите без --dry-run для реальной записи.")


if __name__ == "__main__":
    main()