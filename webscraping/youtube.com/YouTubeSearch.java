// https://kaijento.github.io/2017/05/19/web-scraping-youtube.com/
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import java.io.IOException;

public class YouTubeSearch {

    public static void main (String[] args) throws IOException {

        String url   = "http://www.youtube.com/results";
        String query = "dj liquid raving";

        Document doc = Jsoup.connect(url)
            .data("search_query", query)
            .userAgent("Mozilla/5.0")
            .get();

        for (Element a : doc.select(".yt-lockup-title > a[title]:not([href*=&list=])")) {
            System.out.println(
                "http://www.youtube.com" + a.attr("href") + " " + a.attr("title")
            );
        }

    }
}
