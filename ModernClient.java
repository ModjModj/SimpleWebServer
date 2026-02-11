import java.io.*;
import java.net.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ModernClient {
    public static void main(String[] args) {
        String serverAddress = "localhost";
        int port = 8000;
        int connectionCount = 1000000;

        ExecutorService executor = Executors.newFixedThreadPool(connectionCount);

        for (int i = 0; i < connectionCount; i++) {
            final int id = i;
            executor.execute(() -> {
                try (Socket socket = new Socket(serverAddress, port)) {
                    System.out.println("Connection " + id + " established.");
                    
                    // Simple interaction: send a message
                    PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                    out.println("Hello from connection " + id);
                   
                } catch (IOException e) {
                    System.err.println("Connection " + id + " failed: " + e.getMessage());
                }
            });
        }
        executor.shutdown();
    }
}
