import os
import requests


def send_telegram_notification(order):
    token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '')

    if not token or not chat_id:
        print("Telegram Token или Chat ID не настроены в .env")
        return False

    # Формируем ссылки на карты (если координаты переданы)
    if order.lat and order.lng:
        google_maps_url = f"https://maps.google.com/?q={order.lat:.6f},{order.lng:.6f}"
        yandex_maps_url = f"https://yandex.ru/maps/?pt={order.lng:.6f},{order.lat:.6f}&z=16"
        maps_text = (
            f"🗺 <b>Локация покупателя:</b>\n"
            f"👉 <a href='{google_maps_url}'>Открыть в Google Maps</a>\n"
            f"👉 <a href='{yandex_maps_url}'>Открыть в Yandex Maps</a>"
        )
    else:
        maps_text = "🗺 <b>Локация:</b> Не указана"

    # Формируем список товаров
    items_text = ""
    for item in order.items.all():
        items_text += f"• <b>{item.product_name}</b> — {item.quantity} шт. ({item.price:,.0f} сум)\n"

    # Форматируем дату и время доставки
    delivery_date_str = order.delivery_date.strftime('%d.%m.%Y') if getattr(order, 'delivery_date', None) else 'Не указана'
    delivery_slot_str = getattr(order, 'delivery_slot', 'Не указан')

    message = (
        f"🍰 <b>НОВЫЙ ЗАКАЗ №{order.id}</b>\n\n"
        f"👤 <b>Клиент:</b> {order.customer_name}\n"
        f"📞 <b>Телефон:</b> {order.phone}\n"
        f"💬 <b>Telegram:</b> {order.telegram or 'Не указан'}\n"
        f"📍 <b>Адрес:</b> {order.address}\n"
        f"📅 <b>Дата доставки:</b> {delivery_date_str}\n"
        f"⏰ <b>Время доставки:</b> {delivery_slot_str}\n\n"
        f"📦 <b>Состав заказа:</b>\n{items_text}\n"
        f"💰 <b>ИТОГО:</b> <b>{order.total_amount:,.0f} сум</b>\n\n"
        f"💬 <b>Комментарий:</b> {order.notes or 'Нет'}\n\n"
        f"{maps_text}"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.ok
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False