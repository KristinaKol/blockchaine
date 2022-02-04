using Aspose.Words;
using CefSharp;
using CefSharp.Handler;
using CefSharp.WinForms;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;


namespace WindowsFormsApp6
{
    public partial class Form1 : Form
    {
        private int indexOfItemUnderMouseToDrop;



        public Form1()
        {

            CefSettings settings = new CefSettings();
            settings.CachePath = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData) + @"\CEF";
            CefSharp.Cef.Initialize(settings);

            InitializeComponent();

            BrowserSettings setting = new BrowserSettings();
            setting.ApplicationCache = CefSharp.CefState.Enabled;
            chromiumWebBrowser1.BrowserSettings = setting;
            chromiumWebBrowser1.Load("http://cloud-computing.tasty-catalog.ru/?v=1");




            chromiumWebBrowser1.DownloadHandler = new DownloadHandler();
        }








        private void chromiumWebBrowser1_ConsoleMessage(object sender, ConsoleMessageEventArgs e)
        {
            if (e.Message.ToLower().IndexOf("error") != -1)
            {
                chromiumWebBrowser1.Load("http://cloud-computing.tasty-catalog.ru/?v=1");
            }
            string[] command = e.Message.Split('|');
            if (command[0] == "command")
            {
                switch (command[1])
                {




                    //ПРОВЕРКА ФАЙЛОВ
                    case "CHECK_SYSTEM":

                        //скачиваем цепочку блокчейн
                        //<путь файла , hash>
                        Dictionary<string, string> block = Server.GetBlocks(command[1]);
                        //скачиваем файлы с сервера
                        string[] files = Server.GetFiles(command[1]);

                        //перебираем файлы
                        foreach (string f in files)
                        {
                            //есть файл в блокчейне 
                            if (block.ContainsKey(f))
                            {
                                if (md5(f) != block[f])
                                {
                                    //помечаем как ошибку
                                    Server.AddError(f);
                                }
                            }
                            else
                            {
                                //помечаем как ошибку

                                Server.AddError(f);
                            }
                        }

                        break;
                    //ЗАГРУЗКА ФАЙЛА НА СЕРВЕР
                    case "UPLOAD_FILE":
                        OpenFileDialog fd = new OpenFileDialog();
                        //открыть диалог выбора файлов
                        if (fd.ShowDialog() == DialogResult.OK)
                        {
                            //ЗАЩИФРОВАЛИ ФАЙЛ
                            AES.encrypt(fd.FileName);
                            //ПОЛУЧИЛИ КЛЮЧ ШИФРОВАНИЯ AES
                            string keyAESsend = File.ReadAllText("key_tmp.key");
                            //ВЫПОЛНИЛИ ГЕНЕРАЦИЮ КЛЮЧЕЙ ПО Д/Х И ПОЛУЧИЛИ МАССИВ ОТКРЫТЫХ КЛЮЧЕЙ RSA

                            //в эту функцию мы передаем id хранилища
                            string[] keysDH = DH.getKeys(command[1]);
                            //ЗАЩИФРОВАЛИ AES КЛЮЧ И ПОЛУЧИЛИ МАССИВ КЛЮЧЕЙ ПОД КАЖДОГО ПОЛЬЗОВАТЕЛЯ ХРАНИЛИЩА 
                            string[] keysRSA = RSA.encrypt(keyAESsend, keysDH);
                            //ОТПРАВИЛИ ФАЙЛ И КЛЮЧИ
                            sendFile("file_tmp.data", keysRSA);

                        }


                        break;
                    //СКАЧИВАНИЕ ФАЙЛА
                    case "LOAD_FILE":
                        //скачивает файл
                        //id файла И id текущего пользователя
                        getFile(command[1], command[2]);

                        //сохраняем зашифрованный ключ
                        string key = File.ReadAllText("key_tmp.key");
                        //ключ по ДХ
                        string keyDH = File.ReadAllText("DH_KEYS.data");

                        //расшифровываем ключ aes
                        byte[] keyAES = RSA.decrypt(key, keyDH);
                        //расшифровываем файл
                        byte[] file = AES.decrypt("file_tmp.data", keyAES);

                        //и сохраняем его
                        SaveFileDialog sd = new SaveFileDialog();
                        if (sd.ShowDialog() == DialogResult.OK)
                        {
                            File.WriteAllBytes(sd.FileName, file);
                        }

                        break;



                }

            }
        }









        //СДЕЛАТЬ ОКНО НА ВЕСЬ ЭКРАН
        private void Form1_Load(object sender, EventArgs e)
        {
            this.WindowState = FormWindowState.Maximized;
            DH.getPersonalKey();
        }




        private string md5(string path)
        {
            return "";
        }


        private string getFile(string idFile, string token, string options = "")
        {
            return "";
        }

        private string sendFile(string path, string[] keys, string options = "")
        {

            WebClient fileUpload = new WebClient();
            try
            {
                byte[] responce = fileUpload.UploadFile("http://tasty-catalog.ru/catalog/load/?" + options, path);
                return Encoding.UTF8.GetString(responce);
            }
            catch (WebException ex)
            {
                String responseFromServer = ex.Message.ToString() + " ";
                if (ex.Response != null)
                {
                    using (WebResponse response = ex.Response)
                    {
                        Stream dataRs = response.GetResponseStream();
                        using (StreamReader reader = new StreamReader(dataRs))
                        {
                            responseFromServer += reader.ReadToEnd();
                        }
                    }
                }

                return "";

            }
        }

        private void chromiumWebBrowser1_LoadingStateChanged(object sender, LoadingStateChangedEventArgs e)
        {

        }
    }
    public class DownloadHandler : IDownloadHandler
    {
        public event EventHandler<DownloadItem> OnBeforeDownloadFired;

        public event EventHandler<DownloadItem> OnDownloadUpdatedFired;

        public void OnBeforeDownload(IWebBrowser chromiumWebBrowser, IBrowser browser, DownloadItem downloadItem, IBeforeDownloadCallback callback)
        {
            OnBeforeDownloadFired?.Invoke(this, downloadItem);

            if (!callback.IsDisposed)
            {
                using (callback)
                {
                    callback.Continue(downloadItem.SuggestedFileName, showDialog: true);
                }
            }
        }

        public void OnDownloadUpdated(IWebBrowser chromiumWebBrowser, IBrowser browser, DownloadItem downloadItem, IDownloadItemCallback callback)
        {
            OnDownloadUpdatedFired?.Invoke(this, downloadItem);
        }


    }
}