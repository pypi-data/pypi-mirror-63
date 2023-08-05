# wichaya Library (PAN)

สวัสดครับ นี่ป่านเอง ไลบรารี่นี้ใช้สำหรับฝึกสร้างไลบรารี่เป็นของตัวเอง ความสามารถคือ

  - แสดงชื่อภาษาอังกฤษ 
  - แสดงชื่อภาษาไทย


### วิธีติดตั้งแสนง่าย


เราจะติดตั้งผ่านเจ้า pip

```sh
pip install wichaya
```

ง่ายไหมล่ะ

วิธีใช้ก็ง่ายมาก
- เปิด Python แล้วพิพม์ตามนี้เลย

```sh
from wichaya import wichaya

Pan = Wichaya()

	print(help(Pan.WhoIAm))

	print(Pan) #print object name to show __str__
	print(Pan.name)
	print(Pan.lastname)
	print(Pan.nickname)
	Pan.WhoIAm()
	print(Pan.email) #ใช้ @property เพื่อแปลง def ให้เวลาเรียกใช้ไม่ต้องใส่ ()

	print("---------")

	pp = Wichaya()
	pp.WhoIAm()
	pp.name = "วิชญะ"
	pp.lastname = "จารุจินดา"
	pp.nickname = "ป่าน"


	print(pp.name)
	print(pp.lastname)
	print(pp.nickname)

	pp.WhoIAm()

```

| สร้างไฟล์ README  | https://dillinger.io/ |
