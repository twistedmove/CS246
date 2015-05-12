package edu.stanford.cs246.HW1P1;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map.Entry;

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

public class MapReduce extends Configured implements Tool {
	public static void main(String[] args) throws Exception {
		System.out.println(Arrays.toString(args));
		int res = ToolRunner.run(new Configuration(), new MapReduce(), args);

		System.exit(res);
	}

	@Override
	public int run(String[] args) throws Exception {
		System.out.println(Arrays.toString(args));
		Job job = new Job(getConf(), "Friendlist");
		job.setJarByClass(MapReduce.class);
		job.setOutputKeyClass(IntWritable.class);
		job.setOutputValueClass(Text.class);

		job.setMapperClass(Map.class);
		job.setReducerClass(Reduce.class);

		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));

		job.waitForCompletion(true);

		return 0;
	}

	public static class Map extends Mapper<LongWritable, Text, IntWritable, Text> {
		private IntWritable word = new IntWritable();
		private Text recommendations = new Text();

		@Override
		public void map(LongWritable key, Text value, Context context)
				throws IOException, InterruptedException {

			for (String token : value.toString().split("\\n+")) {
				String[] userID = token.split("\\t", -1);
				int username = Integer.parseInt(userID[0]);
				if (userID[1].isEmpty()) {
					word.set(username);
					recommendations.set(userID[0] + "\t" + "N"); // flag to indicate users who do not have friends 
					context.write(word, recommendations); 				
				}
				else {
					word.set(username);
					for (String neighbour : userID[1].split(",")) {
						recommendations.set(neighbour + "\t" + "F"); // flag to indicate immediate connections 
						context.write(word, recommendations); 
					}

					for (String neighbour : userID[1].split(",")) {
						for (String neighbour1 : userID[1].split(",")) {
							if (!neighbour.equals(neighbour1)) {
								word.set(Integer.parseInt(neighbour));
								recommendations.set(neighbour1 + "\t" + "R"); // flag to indicate recommendations
								context.write(word, recommendations);
							}
						}
					}
				}
			}
		}
	}

	public static class Reduce extends Reducer<IntWritable, Text, IntWritable, Text> {
		private Text output = new Text();
		private IntWritable userID = new IntWritable();

		@Override
		public void reduce(IntWritable key, Iterable<Text> values, Context context)
				throws IOException, InterruptedException {
			userID = key;
			HashMap<Integer, Integer> network = new HashMap<Integer, Integer>();
			for (Text value : values) {
				String[] split = value.toString().split("\t");
				int friendname = Integer.parseInt(split[0]);
				if (split[1].contains("F")) { // flag immediate connections
					network.put(friendname, -1);
				}
				else if (split[1].contains("R")) { // add to recommendation list
					if (network.containsKey(friendname) && network.get(friendname) != -1) {
						network.put(friendname, network.get(friendname) + 1);
					} else if (!network.containsKey(friendname)){
						network.put(friendname, 1);;
					}					
				}
				else if (key.get() == Integer.parseInt(split[0])) {	
					// output empty list of recommendations when users do not have any friends
					output.set("");
					context.write(userID, output);
					return;
				}
			}
			
			List<java.util.Map.Entry<Integer, Integer>> greatest = new ArrayList<java.util.Map.Entry<Integer, Integer>>(network.entrySet());
			Comparator<java.util.Map.Entry<Integer, Integer>> comp = new Comparator<java.util.Map.Entry<Integer, Integer>>(){

				@Override
				public int compare(java.util.Map.Entry<Integer, Integer> o1, java.util.Map.Entry<Integer, Integer> o2) {  
					// compare value in the map<Integer, Integer>
					if (o2.getValue() == o1.getValue()) {
						return o1.getKey() - o2.getKey();
					}
					else 
						return o2.getValue() - o1.getValue();
				}
			};

			// sort recommendations based on value
			Collections.sort(greatest, comp);
			int start = 0;
			for (java.util.Map.Entry<Integer, Integer> loop : greatest) {
				if (loop.getValue() == -1)
					break;
				else
					start++;
			}
			
			greatest = greatest.subList(0, start);
			String stringoutput = "";
			// output top recommendations
			for (int i = 0; i < 10 && i < greatest.size(); i++) {
				stringoutput += greatest.get(i).getKey().toString() + ",";
			}
			if (stringoutput != "") 
				stringoutput = stringoutput.substring(0, stringoutput.length() - 1);;
			output.set(stringoutput);
			context.write(userID, output);
		}
	}
}

