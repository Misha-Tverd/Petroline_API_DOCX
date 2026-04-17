# Petroline Word Generator

Мінімальний готовий проект для генерації `.docx` файлів по транзакціях Petroline.

## Що робить
- бере транзакції з `POST /api/TrkTransactions/list`
- перевіряє критичні поля: `driver`, `vehicle`, `liters`
- якщо поля відсутні — записує запис у `logs/missing_fields_log.json`
- якщо запис валідний — створює 2 однакові `.docx`:
  - у папці техніки
  - у папці водія
- запам'ятовує вже оброблені записи в `data/processed_ids.json`

## Встановлення
```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Налаштування
1. Скопіюй `.env.example` у `.env`
2. Для локального тесту залиш:
```env
USE_SAMPLE_DATA=true
```
3. Для реального API постав:
```env
USE_SAMPLE_DATA=false
PETROLINE_LOGIN=...
PETROLINE_PASSWORD=...
```

## Запуск
```bash
python main.py
```

## Теги у шаблоні Word
Шаблон `templates/template.docx` використовує такі теги:
- `{{ date }}`
- `{{ driver }}`
- `{{ vehicle }}`
- `{{ fuel }}`
- `{{ liters }}`
- `{{ amount }}`
- `{{ azs }}`
- `{{ transaction_id }}`
- `{{ card1_number }}`
- `{{ card2_number }}`
- `{{ recipient }}`
