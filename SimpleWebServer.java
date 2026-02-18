import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class SimpleWebServer {

  public static void main(String[] args) throws IOException {
    HttpServer server = HttpServer.create(new InetSocketAddress(8000), 0);
    server.createContext("/", new StaticFileHandler(Paths.get("."))); // serve from project root
    server.setExecutor(null);
    server.start();
    System.out.println("Server is running on http://localhost:8000/");
  }

  static class StaticFileHandler implements HttpHandler {
    private final Path baseDir;

    StaticFileHandler(Path baseDir) {
      this.baseDir = baseDir.toAbsolutePath().normalize();
    }

    @Override
    public void handle(HttpExchange exchange) throws IOException {
      String requestPath = exchange.getRequestURI().getPath(); // e.g. "/styles/shared/general.css"

      if (requestPath.equals("/")) {
        requestPath = "/index.html";
      }

      // Prevent path traversal like /../
      Path filePath = baseDir.resolve(requestPath.substring(1)).normalize();
      if (!filePath.startsWith(baseDir) || !Files.exists(filePath) || Files.isDirectory(filePath)) {
        byte[] notFound = "404 Not Found".getBytes();
        exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=UTF-8");
        exchange.sendResponseHeaders(404, notFound.length);
        try (OutputStream os = exchange.getResponseBody()) {
          os.write(notFound);
        }
        return;
      }

      byte[] bytes = Files.readAllBytes(filePath);
      String contentType = Files.probeContentType(filePath);
      if (contentType == null) {
        contentType = guessContentType(filePath.toString());
      }

      exchange.getResponseHeaders().set("Content-Type", contentType);
      exchange.sendResponseHeaders(200, bytes.length);
      try (OutputStream os = exchange.getResponseBody()) {
        os.write(bytes);
      }
    }

    private String guessContentType(String filename) {
      String f = filename.toLowerCase();
      if (f.endsWith(".css")) return "text/css; charset=UTF-8";
      if (f.endsWith(".js")) return "application/javascript; charset=UTF-8";
      if (f.endsWith(".png")) return "image/png";
      if (f.endsWith(".jpg") || f.endsWith(".jpeg")) return "image/jpeg";
      if (f.endsWith(".gif")) return "image/gif";
      if (f.endsWith(".svg")) return "image/svg+xml";
      if (f.endsWith(".html")) return "text/html; charset=UTF-8";
      return "application/octet-stream";
    }
  }
}
