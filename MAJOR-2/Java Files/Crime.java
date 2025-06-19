import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import javax.imageio.ImageIO;
import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollBar;
import javax.swing.JScrollPane;
import javax.swing.SwingUtilities;
import javax.swing.Timer;
import javax.swing.border.EmptyBorder;
public class Crime extends JFrame 
{
    public JPanel imagePanel;
    public String[] imagePaths = 
    {
        "D:\\MAJOR-2\\Java Files\\Images\\Barricade.jpg",
        "D:\\MAJOR-2\\Java Files\\Images\\Fingerprints.jpg",
        "D:\\MAJOR-2\\Java Files\\Images\\Forensics.jpg",
        "D:\\MAJOR-2\\Java Files\\Images\\Interrogation.jpg",
        "D:\\MAJOR-2\\Java Files\\Images\\Map.jpg",
        "D:\\MAJOR-2\\Java Files\\Images\\Search.jpg",
        "D:\\MAJOR-2\\Java Files\\Images\\Computers.png",
        "D:\\MAJOR-2\\Java Files\\Images\\Criminal.png",
        "D:\\MAJOR-2\\Java Files\\Images\\Detective.png",
        "D:\\MAJOR-2\\Java Files\\Images\\Finders.png",
    };
    public Timer timer;
    public JScrollPane scrollPane;
    public Crime() 
    {
        setTitle("Crime Investigation");
        setSize(1000, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());
        JLabel flagLabel = new JLabel(new ImageIcon
        (
            new ImageIcon("D:\\MAJOR-2\\Java Files\\Images\\Indian Flag.png")
                .getImage().getScaledInstance(2000, 500, Image.SCALE_SMOOTH)
        ));
        flagLabel.setHorizontalAlignment(JLabel.CENTER);
        add(flagLabel, BorderLayout.NORTH);
        imagePanel = new JPanel();
        imagePanel.setLayout(new FlowLayout(FlowLayout.LEFT, 7, 2));
        imagePanel.setBackground(Color.BLACK);
        for (int i = 0; i < 2; i++) 
        {
            for (String path : imagePaths) 
            {
                imagePanel.add(createImageLabel(path));
            }
        }
        scrollPane = new JScrollPane(imagePanel);
        scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
        scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_NEVER);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        scrollPane.setPreferredSize(new Dimension(1000, 260));
        add(scrollPane, BorderLayout.CENTER);
        JPanel buttonPanel = new JPanel();
        buttonPanel.setBackground(new Color(30, 30, 30));
        buttonPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
        JButton analysisButton = createStyledButton("Crime Analysis", new Color(173, 216, 230));
        analysisButton.addActionListener(e -> runPythonScript("D:\\MAJOR-2\\Python Files\\CRIME.py"));
        JButton heatmapButton = createStyledButton("Generate Chart", new Color(144, 238, 144));
        heatmapButton.addActionListener(e -> runPythonScript("D:\\MAJOR-2\\Python Files\\Chart.py"));
        buttonPanel.add(analysisButton);
        buttonPanel.add(Box.createHorizontalStrut(20));
        buttonPanel.add(heatmapButton);
        add(buttonPanel, BorderLayout.SOUTH);
        timer = new Timer(1, e -> moveImages());
        timer.start();
        setVisible(true);
    }
    public JLabel createImageLabel(String imagePath) 
    {
        try 
        {
            BufferedImage img = ImageIO.read(new File(imagePath));
            Image scaled = img.getScaledInstance(250, 250, Image.SCALE_SMOOTH);
            return new JLabel(new ImageIcon(scaled));
        } 
        catch (IOException e) 
        {
            e.printStackTrace();
            return new JLabel("Error");
        }
    }
    public void moveImages() 
    {
        JScrollBar bar = scrollPane.getHorizontalScrollBar();
        bar.setValue(bar.getValue() + 1);
        if (bar.getValue() >= bar.getMaximum() - scrollPane.getViewport().getWidth()) 
        {
            bar.setValue(0);
        }
    }
    private JButton createStyledButton(String text, Color backgroundColor) 
    {
        JButton button = new JButton(text);
        button.setFocusPainted(false);
        button.setFont(new Font("SansSerif", Font.BOLD, 14));
        button.setBackground(backgroundColor);
        button.setForeground(Color.BLACK);
        button.setPreferredSize(new Dimension(180, 40));
        button.setBorder(BorderFactory.createLineBorder(Color.DARK_GRAY, 1, true));
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        return button;
    }
    private void runPythonScript(String scriptPath) 
    {
        try 
        {
            ProcessBuilder builder = new ProcessBuilder("python", scriptPath);
            builder.redirectErrorStream(true);
            Process process = builder.start();
            new Thread(() -> 
            {
                try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) 
                {
                    String line;
                    while ((line = reader.readLine()) != null) 
                    {
                        System.out.println(line);
                    }
                } 
                catch (IOException e) 
                {
                    e.printStackTrace();
                }
            }).start();
        } 
        catch (IOException e) 
        {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) 
    {
        SwingUtilities.invokeLater(Crime::new);
    }
}