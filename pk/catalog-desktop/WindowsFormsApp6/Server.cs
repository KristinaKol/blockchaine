using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace WindowsFormsApp6
{
    class Server
    {

        //ОТПРАВИТЬ СВОЙ КЛЮС диффи хелмана
        public static string SendDHKey(string key)
        {
            WebClient server= new WebClient();
            return server.DownloadString(
                String.Format("http://test.tasty-catalog.ru/keys/addDH/?key={0}", key));

        }


        //ОТПРАВИТЬ ОШИБКУ О ФАЙЛЕ
        public static string AddError(string file)
        {
            WebClient server = new WebClient();
            return server.DownloadString(
                String.Format("http://test.tasty-catalog.ru/catalog/addError/?file={0}", file));
        }

        //ЗАПРОС К СЕРВЕРУ ДЛЯ ЗАГРУЗКИ ЦЕПИ БЛОКЧЕЙН
        public static Dictionary<string, string> GetBlocks(string store)
        {

            Dictionary<string, string> result = new Dictionary<string, string>();
            WebClient server = new WebClient();
            string responce =  server.DownloadString(
                String.Format("http://test.tasty-catalog.ru/catalog/getBlocks/?store_id={0}", store));


            string[] blocks = responce.Split('|');
            foreach(string b in blocks)
            {
                string[] data = b.Split('~');
                result.Add(data[0], data[1]);
            }

            return result;

        }

        //ЗАПРОС К СЕРВЕРУ ДЛЯ ЗАГРУЗКИ ФАЙЛОВ
        public static string[] GetFiles(string store)
        {
            WebClient server = new WebClient();
            string responce = server.DownloadString(
                String.Format("http://test.tasty-catalog.ru/catalog/getFiles/?store_id={0}", store));
            string[] files = responce.Split('|');

            foreach(string file in files)
            {
                server.DownloadFile(file, "tmp/" + file);
            }
            return files;
        }
    }
}
