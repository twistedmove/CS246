package edu.stanford.cs246.kmeancluster;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class Kmeancluster extends Configured implements Tool {
	static String dir = "/home/cloudera/workspace/kmeancluster/";
	
	public static void main(String[] args) throws Exception {
		int res = 0;
		// set number of iterations to be 20
		for (int i = 0; i < 20; i++) {
			args[2] = "" + i;
			res = ToolRunner.run(new Configuration(), new Kmeancluster(), args); 	
		}
		System.exit(res);
	}

	@Override
	public int run(String[] args) throws Exception {
		int i = Integer.valueOf(args[2]);
		Job job = new Job(getConf(), "Kmeancluster");
		Configuration config = job.getConfiguration();
		// set input and output directories
		config.set("inputDirectory", dir + "random" + i + ".txt");
		config.set("outputDirectory", dir + "random" + (i + 1) + ".txt");
		
		Path inputPath = new Path(args[0]);
		Path outputPath = new Path(args[1] + i);
		job.setJarByClass(Kmeancluster.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);
		
		job.setMapperClass(Map.class);
		job.setReducerClass(Reduce.class);
		job.setMapOutputKeyClass(IntWritable.class);
		job.setMapOutputValueClass(Text.class);

		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);

		FileInputFormat.setInputPaths(job, inputPath);
		FileOutputFormat.setOutputPath(job, outputPath);

		job.waitForCompletion(true);

		return 0;
	}

	// helper function to convert array of string to array of Double
	public static Double[] stringToDoubleArray(String[] strings) {
		Double[] numbers = new Double[strings.length];
		for (int i = 0; i < strings.length; i++) {
			numbers[i] = Double.parseDouble(strings[i]);
		}
		return numbers;
	}
	
	public static class Map extends Mapper<LongWritable, Text, IntWritable, Text> {
		private IntWritable clusternumber = new IntWritable();
		private Text features = new Text();
		ArrayList<Double[]> currentCluster = new ArrayList<Double[]>();
		public void setup(Context context) throws IOException {
			String inputPath = context.getConfiguration().get("inputDirectory");
			// read current cluster file
			BufferedReader br = new BufferedReader(new FileReader(inputPath));
			try {
		        String line = br.readLine();
		        while (line != null) {
		            String[] features = line.split("\\s", -1);
		            currentCluster.add(stringToDoubleArray(features));
		            line = br.readLine();
		        }
		    } finally {
		        br.close();
		    }
		}
		double totalCost = 0;
		@Override
		public void map(LongWritable key, Text value, Context context)
				throws IOException, InterruptedException {
			for (String token: value.toString().split("\\n+")) {
				String[] documents = token.split("\\s", -1);
				Double[] feature = stringToDoubleArray(documents);
				List<Double> distances = calculateDistance(feature, currentCluster);
				// classify the point in the cluster whose centroid it has the smallest Euclidean distance from
				int index = 1;
				double min = distances.get(0); 
				for (int i = 1; i < distances.size(); i++) {
					if (distances.get(i) < min) {
						min = distances.get(i);
						index = i + 1;
					}			
				}
				// output cluster number as key, original line of features as value
				clusternumber.set(index);
				features.set(token);
				context.write(clusternumber, features);
				// calculate cost function for each point
				totalCost += Math.pow(min,2);
			}
			// append to the file
			BufferedWriter bwf = new BufferedWriter(new FileWriter("costFunctionC1.txt", true));
			bwf.write(totalCost + "\n");
			bwf.close();
		}

		// helper function to calculate Euclidean distances of one point from 10 current centroids
		private List<Double> calculateDistance(Double[] feature, ArrayList<Double[]> currentCluster) {
			List<Double> clusterDistance = new ArrayList<Double>();
			for (Double[] cluster : currentCluster) {
				double distance = 0;
				for (int i = 0; i < cluster.length; i++) {
					distance += Math.pow(cluster[i] - feature[i], 2);
				}
				clusterDistance.add(Math.sqrt(distance));
			}			
			return clusterDistance;
		}
	}

	public static class Reduce extends Reducer<IntWritable, Text, Text, Text> {
		private Text clusterFeature = new Text();
		private Text ignore = new Text();
		@Override
		public void reduce(IntWritable key, Iterable<Text> values, Context context)
				throws IOException, InterruptedException {
			List<Double> sum = new ArrayList<Double>();
			for (int i = 0; i < 58; i++) {
				sum.add(0.0);
			}
			int counter = 0;
			// calculate the sum of features of each cluster
			for (Text val : values) {
				counter++;
				String[] value = val.toString().split("\\s", -1);
				Double[] numbers = stringToDoubleArray(value);
				for (int i = 0; i < numbers.length; i++) {
					sum.set(i, sum.get(i) + numbers[i]);
				}
			}
			// calculate the average of features of each cluster
			for (int i = 0; i < sum.size(); i++) {
				sum.set(i, sum.get(i) / counter);
			}
			String[] stringOfFeatures = doubleToStringArray(sum);
			String output = "";
			for (String str : stringOfFeatures) {
				output += " " + str;
			}
			output = output.substring(1);
			// output updated cluster as key
			clusterFeature.set(output);
			ignore.set("");
			context.write(clusterFeature, ignore);
			// write updated cluster to output directory
			String outputPath = context.getConfiguration().get("outputDirectory");
			BufferedWriter bw = new BufferedWriter(new FileWriter(outputPath, true));
			bw.write(output + "\n");
			bw.close();
		}
		// helper function to convert array of Double to array of String
		private String[] doubleToStringArray(List<Double> doubles) {
			String[] strings = new String[doubles.size()];
			for (int i = 0; i < doubles.size(); i++) {
				strings[i] = (doubles.get(i)).toString();
			}
			return strings;
		}
	}
}

