# helpdesk
Helpdesk in security business
CRM для обслуживающей компании. Заточено под обслуживание оборудования ЧОП.
В настоящее время работает в нескольких городах с одним сервером. Более 50 пользователей. Сколько угодно обслуживающих филиалов. Удобное переключение между 
филиалами по списку доступному каждому пользователю в отдельности. Групповые политики регламентируют доступ на запись/чтение.
Доступ инженерам в программу осуществлен через отдельную страницу с личного смартфона. Там они могут просмотреть задания, отчитаться о проделанной работе - что снижает нагрузку на менеджера в конце рабочего дня. Планируется переход на API.
19.12.2022. API на DRF добавлено. Доступны такие API: авторизация по сессиям, задачи для инженеров (список задач+описание отдельной задачи(+история по объекту)), для руководителя (распределение списка задач по инжененерам и контроля выполнения, преимущественно в выходные и праздничные дни), а также для реализации доски Канбан. В ближайшем будущем планируется создать приложение для инженеров под Android.
