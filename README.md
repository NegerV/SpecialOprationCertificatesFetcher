# SpecialOprationCertificatesFetcher
A tool to fetch certificates for special operations data from [特种作业操作证及安全生产知识和管理能力考核合格信息查询平台](https://cx.mem.gov.cn), using python+tesseract-OCR

1. You should install `tesseract-OCR` first.
2. Then you should change the parameter: `pytesseract.pytesseract.tesseract_cmd` to your `tesseract.exe`'s path.
3. Next, verify if `data.csv` exists in the directory. If exists, delete it.
4. Start fetchers.py. Because of the dummy recognition capability of `tesseract-OCR`, this program may interrupt frequently. So, when it interrupt, you can find line 55: `for lst in code2name_list[:]:`, and change the left border to the count which you can find in running terminal.
5. After completing the above operations， you can find a file named `data.csv`, you may veritify if exists duplicate entries.
6. All right, the last step: click the `csv2xls.py`, and you can find the final sheet!







Well, the captcha identification is not good.

Maybe I will change it by using api? orz
